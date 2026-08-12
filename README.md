[c_icap.py] iter 1: FAIL ▒ no finding with a known version for PRODUCT='c-icap'
[c_icap.py] iter 2: FAIL ▒ no finding with a known version for PRODUCT='c-icap'
[c_icap.py] iter 3: FAIL ▒ no finding with a known version for PRODUCT='c-icap'
[c_icap.py] gave up after 3 iterations ▒ left untouched. Last diagnostic:
PRODUCT token = 'c-icap'   repo token (from LINK_SOURCE) = 'c-icap-server'
candidate files scanned by engine: 165
  strictly owned (path segment == PRODUCT/repo-token, or SOURCE_FILENAME_PATTERNS match): 165
  weakly owned (fuzzy path segment match + dir has >=3 source files): 0
  canon-version-file auto owned (VERSION/CMakeLists.txt/etc. whose content literally mentions the token): 0

=> Files ARE owned. Showing what check_file_versions_only()/check_meta() actually returned on them (empty = CONTAINS/VERSION_PATTERNS problem):
  access.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  acl.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  array.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  aserver.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  body.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  build.sh -> []
  build_tests.sh -> []
  cache.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  cfg_lib.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  cfg_param.c -> []
    nearby content that looks version-like:
      t under the terms of the GNU Lesser General Public
       *  License as published by the Free Software Foundation; either
       *  version 2.1 of the License, or (at your option) any later version.
       *
       *  This program is distributed in the hope that it will be u
  check_meta(.) -> []
