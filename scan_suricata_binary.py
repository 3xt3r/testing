#!/usr/bin/env python3
import argparse
import json
import mmap
import re
from pathlib import Path

PRINTABLE = set(range(32, 127))

def printable_context(mm, offset, length, radius=100):
    start = max(0, offset - radius)
    end = min(len(mm), offset + length + radius)
    raw = bytes(mm[start:end])
    return "".join(chr(b) if b in PRINTABLE else "." for b in raw)

def scan(binary_path, dict_path):
    db = json.loads(Path(dict_path).read_text(encoding="utf-8"))
    findings = []
    score = 0
    categories = set()

    with open(binary_path, "rb") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            data_lower = bytes(mm[:]).lower()

            for sig in db["signatures"]:
                needle = sig["pattern"].encode("utf-8").lower()
                pos = 0
                hit_count = 0
                offsets = []

                while True:
                    idx = data_lower.find(needle, pos)
                    if idx < 0:
                        break
                    offsets.append(idx)
                    hit_count += 1
                    pos = idx + 1

                if hit_count:
                    # Score each signature once, regardless of duplicate copies.
                    score += int(sig["weight"])
                    categories.add(sig["category"])
                    findings.append({
                        "pattern": sig["pattern"],
                        "category": sig["category"],
                        "weight": sig["weight"],
                        "count": hit_count,
                        "offsets": [hex(x) for x in offsets[:10]],
                        "context": printable_context(mm, offsets[0], len(needle))
                    })

            # Extract printable ASCII strings and look for version patterns.
            ascii_strings = re.findall(rb"[\x20-\x7e]{5,}", bytes(mm[:]))
            version_hits = []
            for s in ascii_strings:
                text = s.decode("ascii", errors="ignore")
                for rx in db.get("version_regexes", []):
                    for m in re.finditer(rx, text):
                        version_hits.append({
                            "version": m.group(1),
                            "string": text[:500]
                        })

    strong_direct = any(
        f["category"] == "project_identity" and f["weight"] >= 70
        for f in findings
    )

    if strong_direct and (len(categories) >= 2 or score >= 100):
        confidence = "STRONG"
    elif score >= 80 and len(categories) >= 2:
        confidence = "STRONG"
    elif score >= 40 and len(categories) >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "WEAK"

    return {
        "binary": str(binary_path),
        "score": score,
        "categories": sorted(categories),
        "confidence": confidence,
        "version_hits": version_hits,
        "findings": sorted(findings, key=lambda x: (-x["weight"], x["pattern"]))
    }

def main():
    ap = argparse.ArgumentParser(
        description="Heuristic Suricata evidence scanner for stripped binaries"
    )
    ap.add_argument("binary")
    ap.add_argument(
        "--dictionary",
        default=str(Path(__file__).with_name("suricata_binary_dictionary.json"))
    )
    ap.add_argument("-o", "--output", help="Write JSON report")
    args = ap.parse_args()

    result = scan(args.binary, args.dictionary)
    text = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
