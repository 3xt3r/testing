from checkers.base_checker import BaseChecker

class Hpgl2gcode(BaseChecker):
    VENDOR = "roboterbastler"
    PRODUCT = "hpgl2gcode"
    LINK_SOURCE = "https://github.com/Roboterbastler/hpgl2gcode"

    CONTAINS_PATTERNS = [
        r"HP-GL to GCode",
        r"HP-GL.*GCode",
    ]

    SOURCE_FILENAME_PATTERNS = [
        r"(^|/)(README(?:\.md|\.rst|\.txt)?|LICENSE|\.gitignore)$",
        r"(^|/)HP-GL-to-GCode\.pro$",
    ]

    # NOTE: confirmed against the real upstream README.md
    # (github.com/Roboterbastler/hpgl2gcode) -- it contains a single
    # description line ("HP-GL to GCode is a simple converter from a
    # subset of HP-GL code to G code.") and no version number anywhere.
    # This VERSION_PATTERNS regex is kept as a best-effort match in case a
    # future release adds a version string, but there is currently nothing
    # for it to match -- this component may simply have no extractable
    # version upstream, same as highwayhash.
    VERSION_PATTERNS = [
        r"HP-GL to GCode.*v?([0-9]+(?:\.[0-9]+){1,3})",
    ]
