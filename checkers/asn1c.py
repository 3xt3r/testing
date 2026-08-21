from checkers.base_checker import BaseChecker

class Asn1c(BaseChecker):
    VENDOR = "asn1c_project"
    PRODUCT = "asn1c"
    LINK_SOURCE = "https://github.com/vlm/asn1c.git"

    CONTAINS_PATTERNS = [
        r"ASN\.1\s+Compiler",
        r"(?:asn1c.{0,200}Abstract\s+Syntax\s+Notation\s+1|Abstract\s+Syntax\s+Notation\s+1.{0,200}asn1c)",
    ]

    SOURCE_FILENAME_PATTERNS = [
        r"(^|/)configure\.ac$",
    ]

    VERSION_PATTERNS = [
        r"AC_INIT\(\s*\[asn1c\]\s*,\s*\[([^\]]+)\]",
    ]
