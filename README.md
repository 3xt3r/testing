[c_icap.py] enhanced: OK ▒ version='0.5.5' source=C:\Users\a.koltsova\Desktop\NDR\c-icap\include\c-icap-conf.h
--- c_icap.py (original)
+++ c_icap.py (enhanced)
@@ -1,3 +1,4 @@
+# -*- coding: utf-8 -*-
 import os
 import re
 from checkers.base_checker import BaseChecker
@@ -16,6 +17,11 @@
         # fallback (▒▒. RX_AC_INIT ▒▒▒▒) ▒ ▒▒▒▒▒ ▒▒▒▒/▒▒▒▒▒▒ ▒▒▒▒▒▒ ▒▒▒▒▒▒
         # ▒▒▒▒▒▒ ▒▒▒▒▒ ▒ AC_INIT.
         r"(^|/)VERSION\.m4$",
+        # ▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒: include/c-icap-conf.h ▒▒▒▒▒▒▒▒
+        # C_ICAP_HEX_VERSION ▒ ▒▒▒▒▒▒▒▒▒▒▒ hex-▒▒▒▒▒▒. ▒▒▒ ▒▒▒▒▒▒▒▒
+        # ▒▒▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒ ▒ ▒▒▒▒▒▒▒, ▒▒▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒, ▒▒▒
+        # configure.ac/VERSION.m4 (▒▒▒▒ ▒ ▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒).
+        r"(^|/)include/c-icap-conf\.h$",
     ]

     CONTAINS_PATTERNS = [
@@ -38,6 +44,29 @@
         re.IGNORECASE,
     )

+    # ▒▒▒▒▒▒▒▒▒▒▒ hex-▒▒▒▒▒▒ ▒ include/c-icap-conf.h:
+    #   #define C_ICAP_HEX_VERSION 0x000000050005
+    # ▒▒▒▒▒▒: 0x0000MMmmpppp (major, minor, patch ▒ ▒▒ 4 hex-▒▒▒▒▒).
+    # ▒▒▒▒▒▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒ ▒▒ build/c_icap_version.awk:
+    #   major = (hex >> 32) & 0xFFFF
+    #   minor = (hex >> 16) & 0xFFFF
+    #   patch = hex & 0xFFFF
+    # ▒▒▒▒▒▒: 0x000000050005 -> major=0, minor=5, patch=5 -> "0.5.5"
+    RX_HEX_VERSION = re.compile(
+        r"#\s*define\s+C_ICAP_HEX_VERSION\s+0x([0-9A-Fa-f]{12})"
+    )
+
+    def _decode_hex_version(self, hex_str: str):
+        """▒▒▒▒▒▒▒▒▒▒▒▒ 12-▒▒▒▒▒▒▒ hex-▒▒▒▒▒▒ ▒ ▒▒▒▒▒▒ major.minor.patch."""
+        try:
+            val = int(hex_str, 16)
+        except ValueError:
+            return None
+        major = (val >> 32) & 0xFFFF
+        minor = (val >> 16) & 0xFFFF
+        patch = val & 0xFFFF
+        return f"{major}.{minor}.{patch}"
+
     def check_file_versions_only(self, content: str, path: str):
         if not self.match_source_filename(path):
             return []
@@ -51,15 +80,43 @@
                 return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]
             return []

+        # include/c-icap-conf.h ▒ ▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒ ▒▒▒ ▒ hex-▒▒▒▒▒▒▒.
+        # ▒▒▒ ▒▒▒▒▒ ▒▒▒▒▒▒▒ ▒▒▒▒▒▒, ▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒ ▒▒▒ ▒▒▒▒▒▒.
+        if base == "c-icap-conf.h":
+            m = self.RX_HEX_VERSION.search(s)
+            if m:
+                ver = self._decode_hex_version(m.group(1))
+                if ver:
+                    return [self.make_result(ver, src_abs, extra={"version_source_abs": src_abs})]
+            return []
+
         m = self.RX_AC_INIT.search(s)
         if not m:
             return []
         return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]

     def check_meta(self, directory: str):
-        # VERSION.m4 ▒ ▒▒▒▒▒▒▒▒▒▒ ▒ ▒▒▒ ▒▒, ▒▒▒ ▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒ ▒
-        # AC_INIT ▒ ▒▒▒▒▒▒▒▒. configure.ac ▒ fallback ▒▒▒ ▒▒▒▒▒▒, ▒▒▒
-        # ▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒.
+        # include/c-icap-conf.h ▒ ▒▒▒▒▒▒▒▒▒▒ ▒ ▒▒▒ ▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒ ▒▒▒
+        # ▒ ▒▒▒▒▒▒▒▒▒▒▒ hex-▒▒▒▒▒▒▒. ▒▒▒▒▒▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒ ▒▒
+        # build/c_icap_version.awk (ground truth).
+        conf_h = os.path.join(directory, "include", "c-icap-conf.h")
+        if os.path.isfile(conf_h):
+            try:
+                with open(conf_h, "r", encoding="utf-8", errors="ignore") as f:
+                    text = f.read()
+            except OSError:
+                text = ""
+            m = self.RX_HEX_VERSION.search(text)
+            if m:
+                ver = self._decode_hex_version(m.group(1))
+                if ver:
+                    return [self.make_result(ver, os.path.abspath(conf_h), extra={
+                        "version_source_file": os.path.relpath(conf_h, directory),
+                        "origin": "meta:include/c-icap-conf.h",
+                    })]
+
+        # VERSION.m4 ▒ ▒▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒▒▒: ▒▒▒ ▒▒, ▒▒▒ ▒▒▒▒▒▒▒
+        # ▒▒▒▒▒▒▒▒▒▒▒▒ ▒ AC_INIT ▒ ▒▒▒▒▒▒▒▒.
         version_m4 = os.path.join(directory, "VERSION.m4")
         if os.path.isfile(version_m4):
             try:
@@ -74,6 +131,7 @@
                     "origin": "meta:VERSION.m4",
                 })]

+        # configure.ac ▒ fallback ▒▒▒ ▒▒▒▒▒▒, ▒▒▒ ▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒.
         full = os.path.join(directory, "configure.ac")
         if not os.path.isfile(full):
             return []

[c_icap.py] applied ▒ original backed up to C:\agent_llm_cplus\cpluschecks\checkers\c_icap.py.bak
