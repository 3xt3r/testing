import os
import re
from checkers.base_checker import BaseChecker

class Elasticlient(BaseChecker):
    VENDOR = "seznam"
    PRODUCT = "elasticclient"
    LINK_SOURCE = "https://github.com/seznam/elasticlient.git"

    CONTAINS_PATTERNS = [
        r"Implementation of the theElasticsearch Client",
        r"Elasticsearch Client implementation",
    ]

    # Real CMakeLists.txt (github.com/seznam/elasticlient) does NOT use
    # project(... VERSION x.y.z) at all -- it's just
    # `project(Elasticlient LANGUAGES CXX)`. The actual version pieces come
    # from three separate custom macro calls:
    #   get_variable(ELASTICLIENT_VERSION_MAJOR "..." 2 NO)
    #   get_variable(ELASTICLIENT_VERSION_MINOR "..." 1 NO)
    #   get_variable(ELASTICLIENT_VERSION_PATCH "..." 0 NO)
    RX_MAJOR = re.compile(
        r'get_variable\s*\(\s*ELASTICLIENT_VERSION_MAJOR\s+"[^"]*"\s+(\d+)',
        re.IGNORECASE,
    )
    RX_MINOR = re.compile(
        r'get_variable\s*\(\s*ELASTICLIENT_VERSION_MINOR\s+"[^"]*"\s+(\d+)',
        re.IGNORECASE,
    )
    RX_PATCH = re.compile(
        r'get_variable\s*\(\s*ELASTICLIENT_VERSION_PATCH\s+"[^"]*"\s+(\d+)',
        re.IGNORECASE,
    )

    def _extract_version(self, text: str):
        s = text or ""
        a = self.RX_MAJOR.search(s)
        b = self.RX_MINOR.search(s)
        c = self.RX_PATCH.search(s)
        if a and b and c:
            return f"{a.group(1)}.{b.group(1)}.{c.group(1)}"
        return None

    def check_meta(self, directory: str):
        full = os.path.join(directory, "CMakeLists.txt")
        if not os.path.isfile(full):
            return []
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            return []
        ver = self._extract_version(text)
        if not ver:
            return []
        return [self.make_result(ver, os.path.abspath(full), extra={
            "version_source_abs": os.path.abspath(full),
            "origin": "meta:CMakeLists.txt",
        })]
