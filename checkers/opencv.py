import os
import re

from checkers.base_checker import BaseChecker

class OpenCV(BaseChecker):
    VENDOR = "opencv"
    PRODUCT = "opencv"
    LINK_SOURCE = "https://github.com/opencv/opencv.git"

    CONTAINS_PATTERNS = [
        r"This file is part of OpenCV project\.",
    ]

    SOURCE_FILENAME_PATTERNS = [
        r"(^|/)version\.hpp$",
    ]

    RX_MAJOR = re.compile(r"#define\s+CV_VERSION_MAJOR\s+(\d+)")
    RX_MINOR = re.compile(r"#define\s+CV_VERSION_MINOR\s+(\d+)")
    RX_REV = re.compile(r"#define\s+CV_VERSION_REVISION\s+(\d+)")
    RX_STATUS = re.compile(r'#define\s+CV_VERSION_STATUS\s+"([^"]+)"')

    def _extract_version(self, text: str):
        s = text or ""

        a = self.RX_MAJOR.search(s)
        b = self.RX_MINOR.search(s)
        c = self.RX_REV.search(s)
        if not (a and b and c):
            return None

        ver = f"{a.group(1)}.{b.group(1)}.{c.group(1)}"
        st = self.RX_STATUS.search(s)
        return f"{ver}{st.group(1).strip()}" if st and st.group(1).strip() else ver

    def check_file_versions_only(self, content: str, path: str):
        if not self.match_source_filename(path):
            return []
        ver = self._extract_version(content)
        if not ver:
            return []
        full = os.path.abspath(path)
        return [self.make_result(ver, full, extra={"version_source_abs": full})]

    def check_meta(self, directory: str):
        for rel in (
            # Real path in a raw git checkout of the opencv/opencv repo.
            os.path.join("modules", "core", "include", "opencv2", "core", "version.hpp"),
            # Paths below only exist in an installed/staged tree, kept as
            # fallback in case the scan target is a pre-built install dir.
            os.path.join("opencv2", "core", "version.hpp"),
            os.path.join("include", "opencv2", "core", "version.hpp"),
        ):
            full = os.path.join(directory, rel)
            if not os.path.isfile(full):
                continue

            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception:
                continue

            ver = self._extract_version(text)
            if not ver:
                continue

            return [self.make_result(
                ver,
                full,
                extra={
                    "version_source_abs": full,
                    "origin": f"meta:{rel.replace(os.sep, '/')}",
                },
            )]

        return []
