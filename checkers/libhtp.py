# -*- coding: utf-8 -*-
import os
import re
from checkers.base_checker import BaseChecker

class Libhtp(BaseChecker):
    VENDOR = "oisf"
    PRODUCT = "libhtp"
    LINK_SOURCE = "https://github.com/OISF/libhtp.git"

    CONTAINS_PATTERNS = [
        r"\*\s*@author\s+Ivan\s+Ristic\s*<ivanr@webkreator\.com>",
    ]

    SOURCE_FILENAME_PATTERNS = [
        r"(^|/)VERSION$",
        r"(^|/)(CHANGELOG|ChangeLog|changes|Changes|news|News)(\.[A-Za-z0-9]+)?$",
        # Add configure.ac as a canonical build file that may contain version info
        r"(^|/)configure\.ac$",
        # Add htp_version.h.in as a template that gets the version substituted
        r"(^|/)htp_version\.h\.in$",
    ]

    RX_VERSION = re.compile(
        r"^\s*PKG_VERSION\s*=\s*([0-9]+(?:\.[0-9]+){1,3})\s*$",
        re.MULTILINE,
    )
    RX_CHANGELOG = re.compile(
        r"^\s*([0-9]+(?:\.[0-9]+){1,3})\s*\(\s*\d{1,2}\s+[A-Za-z]+\s+\d{4}\s*\)",
        re.MULTILINE,
    )
    # configure.ac uses m4_esyscmd(./get-version.sh VERSION) which reads PKG_VERSION from VERSION file
    # The actual version is not directly in configure.ac, so we don't add a pattern for it here
    # but we keep the file in SOURCE_FILENAME_PATTERNS for potential future use
    
    # htp_version.h.in has the version as @PACKAGE_VERSION@ which is substituted at build time
    # The actual version value is not present in the template, so we can't extract it directly
    # But we keep the file in SOURCE_FILENAME_PATTERNS for potential future use

    def check_file_versions_only(self, content: str, path: str):
        if not self.match_source_filename(path):
            return []

        s = content or ""
        src_abs = os.path.abspath(path)
        base = os.path.basename(path)

        if base.upper() == "VERSION":
            m = self.RX_VERSION.search(s)
            if m:
                return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]

        if "libhtp" in s.lower():
            m = self.RX_CHANGELOG.search(s)
            if m:
                return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]

        return []