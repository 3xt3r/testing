import os
import re

from checkers.base_checker import BaseChecker

class AlsaLib(BaseChecker):
    VENDOR = "alsa-project"
    PRODUCT = "alsa-lib"
    LINK_SOURCE = "https://github.com/alsa-project/alsa-lib.git"

    STOP_AFTER_FIRST_VERSION = True

    CONTAINS_PATTERNS = [
        r"\*\s*\\author\s+Abramo\s+Bagnara\s+<abramo@alsa-project\.org>",
        r"\*\s*\\author\s+Jaroslav\s+Kysela\s+<perex@perex\.cz>",
    ]

    RX_VERSION = re.compile(
        r"AC_INIT\s*\(\s*\[?alsa-lib\]?\s*,\s*\[?([0-9]+(?:\.[0-9]+){1,3}(?:[A-Za-z][A-Za-z0-9.]*)?)\]?\s*\)",
        re.IGNORECASE,
    )

    def check_meta(self, directory: str):
        full = os.path.join(directory, "configure.ac")
        if not os.path.isfile(full):
            return []

        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            return []

        m = self.RX_VERSION.search(text)
        if not m:
            return []

        return [self.make_result(
            m.group(1),
            os.path.abspath(full),
            extra={
                "version_source_abs": os.path.abspath(full),
                "origin": "meta:configure.ac",
            },
        )]
