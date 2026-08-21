from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|0x[0-9A-Fa-f]+|\d+(?:\.\d+)?|==|!=|<=|>=|&&|\|\||->|::|[{}()\[\];,+*/%&|^!~=<>?:.-]")
CONTROL_WORDS = {"if", "for", "while", "switch", "catch", "else", "do"}
TYPE_WORDS = {"struct", "class", "enum", "union"}


@dataclass(frozen=True, slots=True)
class CodeSegment:
    kind: str
    raw: str
    normalized: str
    exact_hash: str
    normalized_hash: str
    token_count: int
    start_line: int


def _strip_comments(text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(text)
    state = "code"
    quote = ""
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state == "code":
            if ch == "/" and nxt == "/":
                state = "line_comment"
                out.append(" ")
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block_comment"
                out.append(" ")
                i += 2
                continue
            if ch in {'"', "'"}:
                state = "string"
                quote = ch
                out.append(ch)
                i += 1
                continue
            out.append(ch)
            i += 1
            continue
        if state == "line_comment":
            if ch == "\n":
                out.append("\n")
                state = "code"
            i += 1
            continue
        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                out.append(" ")
                i += 2
            else:
                if ch == "\n":
                    out.append("\n")
                i += 1
            continue
        if state == "string":
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                state = "code"
            i += 1
    return "".join(out)


def normalize_segment(text: str) -> str:
    clean = _strip_comments(text.replace("\r\n", "\n").replace("\r", "\n"))
    toks = TOKEN.findall(clean)
    return " ".join(toks)


def _segment(raw: str, kind: str, start_line: int, *, min_tokens: int) -> CodeSegment | None:
    normalized = normalize_segment(raw)
    token_count = len(TOKEN.findall(normalized))
    if token_count < min_tokens:
        return None
    exact_material = "\n".join(line.rstrip() for line in raw.strip().splitlines())
    return CodeSegment(
        kind=kind,
        raw=raw,
        normalized=normalized,
        exact_hash=hashlib.sha256(exact_material.encode("utf-8", errors="ignore")).hexdigest(),
        normalized_hash=hashlib.sha256(normalized.encode("utf-8", errors="ignore")).hexdigest(),
        token_count=token_count,
        start_line=start_line,
    )


def _matching_brace(text: str, open_pos: int) -> int | None:
    depth = 0
    i = open_pos
    state = "code"
    quote = ""
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if state == "code":
            if ch == "/" and nxt == "/":
                state = "line_comment"; i += 2; continue
            if ch == "/" and nxt == "*":
                state = "block_comment"; i += 2; continue
            if ch in {'"', "'"}:
                state = "string"; quote = ch; i += 1; continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
            i += 1
            continue
        if state == "line_comment":
            if ch == "\n": state = "code"
            i += 1; continue
        if state == "block_comment":
            if ch == "*" and nxt == "/": state = "code"; i += 2
            else: i += 1
            continue
        if state == "string":
            if ch == "\\" and i + 1 < len(text): i += 2; continue
            if ch == quote: state = "code"
            i += 1
    return None


def _header_start(text: str, brace_pos: int, max_back: int = 1200) -> int:
    start = max(0, brace_pos - max_back)
    chunk = text[start:brace_pos]
    # Last top-level statement delimiter is a practical function/type header boundary.
    last = max(chunk.rfind(";"), chunk.rfind("}"), chunk.rfind("\n#"))
    return start + last + 1


def _looks_like_function(header: str) -> bool:
    stripped = _strip_comments(header).strip()
    if not stripped or "(" not in stripped or ")" not in stripped:
        return False
    low = stripped.lower()
    if any(re.search(rf"\b{w}\s*\([^)]*\)\s*$", low) for w in CONTROL_WORDS):
        return False
    if any(re.search(rf"\b{w}\b", low) for w in TYPE_WORDS) and ")" not in low.split("{")[-1]:
        return False
    # Exclude initializer lists / lambdas without a stable function-like name where possible.
    before = stripped[: stripped.rfind("(")]
    return bool(re.search(r"(?:operator\s*[^\s]+|[~A-Za-z_][A-Za-z0-9_:<>~]*)\s*$", before))


def extract_segments(text: str, *, min_function_tokens: int = 28, min_type_tokens: int = 24, min_macro_tokens: int = 16) -> list[CodeSegment]:
    segments: list[CodeSegment] = []
    consumed: list[tuple[int, int]] = []

    # Function / type blocks.
    i = 0
    while True:
        brace = text.find("{", i)
        if brace < 0:
            break
        end = _matching_brace(text, brace)
        if end is None:
            break
        hs = _header_start(text, brace)
        header = text[hs:brace]
        low = _strip_comments(header).lower()
        kind = ""
        min_tokens = min_function_tokens
        if _looks_like_function(header):
            kind = "function"
        elif re.search(r"\b(struct|class|enum|union)\b", low):
            kind = "type"
            min_tokens = min_type_tokens
        if kind:
            raw = text[hs:end + 1]
            seg = _segment(raw, kind, text.count("\n", 0, hs) + 1, min_tokens=min_tokens)
            if seg:
                segments.append(seg)
                consumed.append((hs, end + 1))
            # A recognized function/type owns its nested braces; do not emit
            # arbitrary implementation sub-blocks as independent segments.
            i = end + 1
        else:
            # IMPORTANT: an unrecognized outer block is commonly a C++
            # namespace or extern "C" wrapper.  v0.10 jumped to `end + 1`
            # here, which skipped every function/type nested inside it.  Walk
            # into the block instead so header/template-heavy libraries such
            # as Boost and namespace-wrapped projects remain fingerprintable.
            i = brace + 1

    # Preprocessor macro blocks. Useful for public APIs/version-independent identity.
    lines = text.splitlines(keepends=True)
    pos = 0
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if re.match(r"^\s*#\s*define\b", line):
            start = pos
            raw_lines = [line]
            j = idx
            while raw_lines[-1].rstrip().endswith("\\") and j + 1 < len(lines):
                j += 1
                raw_lines.append(lines[j])
            raw = "".join(raw_lines)
            seg = _segment(raw, "macro", idx + 1, min_tokens=min_macro_tokens)
            if seg:
                segments.append(seg)
            # advance positions through consumed lines
            for k in range(idx, j + 1):
                pos += len(lines[k])
            idx = j + 1
            continue
        pos += len(line)
        idx += 1

    # Deduplicate nested/identical representations.
    unique: dict[tuple[str, str], CodeSegment] = {}
    for seg in segments:
        unique.setdefault((seg.kind, seg.normalized_hash), seg)
    return list(unique.values())
