
Package: libodbc2
Architecture: amd64
Version: 2.3.11-2+deb12u1+b2
Multi-Arch: same
Priority: optional
Section: libs
Source: unixodbc (2.3.11-2+deb12u1)
Maintainer: Hugh McMaster <hugh.mcmaster@outlook.com>
Installed-Size: 458
Depends: libc6 (>= 2.17), libltdl7 (>= 2.4.7)
Suggests: odbc-postgresql, tdsodbc
Breaks: libodbc1 (<< 2.3.9-1~)
Replaces: libodbc1 (<< 2.3.9-1~)
Filename: pool/main/u/unixodbc/libodbc2_2.3.11-2+deb12u1+b2_amd64.deb
Size: 150640
MD5sum: f6a33c0309293a5ae47657e4a0a05fb0
SHA1: 0c378087d87e4ea8131b57f67fec194fb66241a6
SHA256: ae3e8c351ec32ad367e90fb795214e2634fc7b1de0447486731a9548eb13db52
Homepage: http://www.unixodbc.org/
Description: ODBC Driver Manager library for Unix
 UnixODBC is an implementation of the Open Database Connectivity standard,
 a database abstraction layer that allows applications to be used with
 many different relational databases by way of a single library.
 .
 This package provides the unixODBC Driver Manager library.
Unsigned-SHA1: 6e2e0d30a38fbb56fd429950c411ec7763326781

Package: libodbccr2
Architecture: amd64
Version: 2.3.11-2+deb12u1+b2
Multi-Arch: same
Priority: optional
Section: libs
Source: unixodbc (2.3.11-2+deb12u1)
Maintainer: Hugh McMaster <hugh.mcmaster@outlook.com>
Installed-Size: 67
Depends: libodbc2 (= 2.3.11-2+deb12u1+b2), libc6 (>= 2.14)
Breaks: libodbc1 (<< 2.3.9-1~)
Replaces: libodbc1 (<< 2.3.9-1~)
Filename: pool/main/u/unixodbc/libodbccr2_2.3.11-2+deb12u1+b2_amd64.deb
Size: 18244
MD5sum: 2ebc3d7ed944df59af0992769d73d224
SHA1: 3f5f2dd6104dd561f1ab4635710f70bcdad224b3
SHA256: b420fc2c2bf2d7b214cbf310163eaf84e9f74cdef1f99ee97348fd56627303a9
Homepage: http://www.unixodbc.org/
Description: ODBC Cursor library for Unix
 UnixODBC is an implementation of the Open Database Connectivity standard,
 a database abstraction layer that allows applications to be used with
 many different relational databases by way of a single library.
 .
 This package provides the unixODBC Cursor library.
Unsigned-SHA1: f221c9f0453dbc679c746b48b289c3d747d2647c

Package: libodbcinst2
Architecture: amd64
Version: 2.3.11-2+deb12u1+b2
Multi-Arch: same
Priority: optional
Section: libs
Source: unixodbc (2.3.11-2+deb12u1)
Maintainer: Hugh McMaster <hugh.mcmaster@outlook.com>
Installed-Size: 101
Depends: unixodbc-common (>= 2.3.11-2+deb12u1+b2), libc6 (>= 2.14), libltdl7 (>= 2.4.7)
Breaks: odbcinst1debian2 (<< 2.3.9-1~)
Replaces: odbcinst1debian2 (<< 2.3.9-1~)
Filename: pool/main/u/unixodbc/libodbcinst2_2.3.11-2+deb12u1+b2_amd64.deb
Size: 34740
MD5sum: a7ea1ee6501e4df04fb521ed9a49420b
SHA1: 96e093b207082de730f348b14b13eebaa4db6a33
SHA256: b31b94cd12aef9b14a3cf94ab0fcf3322b9e06225add5d18fe270dfe6aa2c195
Homepage: http://www.unixodbc.org/
Description: Support library for accessing ODBC configuration files
 UnixODBC is an implementation of the Open Database Connectivity standard,
 a database abstraction layer that allows applications to be used with
 many different relational databases by way of a single library.
 .
 This package contains the odbcinst library from unixODBC, a library
 used by ODBC drivers to read their configuration from /etc/odbcinst.ini
 and the system and user-specific odbc.ini files.
Unsigned-SHA1: 366981b149c1e7aa44d0e52935f36a771b5fb68a
