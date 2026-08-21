import os
import re

from checkers.base_checker import BaseChecker

class Poco(BaseChecker):
    VENDOR = "pocoproject"
    PRODUCT = "poco"
    LINK_SOURCE = "https://github.com/pocoproject/poco.git"

    RX_RC = re.compile(r'#define\s+POCO_VERSION_STR\s+"([\w.\-]+)"')
    RX_VER = re.compile(r"^[vV]?\d+(?:\.\d+){1,4}(?:[-+][0-9A-Za-z._-]+)?$")

    def _read_version_text(self, text: str):
        v = (text or "").strip().splitlines()[0].strip().strip('"').strip("'")
        return v if v and len(v) <= 64 and self.RX_VER.match(v) else None

    def check_file_versions_only(self, content: str, path: str):
        full = os.path.abspath(path)
        norm = full.replace("\\", "/")
        base = os.path.basename(norm).lower()

        if base == "dllversion.rc":
            m = self.RX_RC.search(content or "")
            return [self.make_result(m.group(1).strip(), full, extra={"version_source_abs": full})] if m else []

        if base == "version" and "poco" in norm.lower().split("/"):
            v = self._read_version_text(content)
            return [self.make_result(v, full, extra={"version_source_abs": full})] if v else []

        return []

    def check_file_contains_only(self, content: str, path: str):
        return []

    def check_meta(self, directory: str):
        # NOTE: previously required os.path.basename(directory) == "poco",
        # which breaks on any catalog/scan layout where the context root is
        # not literally named "poco" (e.g. catalog snapshots laid out as
        # poco/reference/...). check_meta is only invoked once this checker
        # has already been shortlisted for the context, so the directory is
        # already known to be poco-relevant; no extra name guard needed here.
        full = os.path.join(directory, "VERSION")
        if not os.path.isfile(full):
            return []

        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                v = self._read_version_text(f.read())
        except Exception:
            return []

        if not v:
            return []

        return [self.make_result(
            v,
            full,
            extra={
                "version_source_abs": full,
                "origin": "meta:poco/VERSION",
            },
        )]
