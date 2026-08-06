
Package: trnet-6.12.47-1-generic
Architecture: amd64
Version: 1.2.0+ci9+b6
Priority: optional
Section: non-free/misc
Source: trnet (1.2.0+ci9)
Maintainer: Alexander V. Gusev <maintainers@astralinux.ru>
Installed-Size: 234
Pre-Depends: dpkg (>= 1.10.24)
Depends: linux-image-6.12.47-1-generic (= 6.12.47-1.astra1+ci8), kmod, trnet-firmware
Filename: pool/non-free/t/trnet/trnet-6.12.47-1-generic_1.2.0+ci9+b6_amd64.deb
Size: 36276
MD5sum: da3fefa691c5172636dad9b54185a10c
SHA1: bc7e691df3267d69d213d38906d4823920179014
SHA256: 12a9c1bd606e2844aae767c1357b209725bdc8d7e222c383e8ed8994969b093b
Description: trnet binary drivers for linux-image-6.12.47-1-generic
 This package contains trnet drivers for the 6.12.47-1-generic Linux kernel,
Unsigned-SHA1: ba19504291d2ed153905d95515a3529bc766cf9c

Package: trnet-firmware
Architecture: all
Version: 1.2.3
Priority: optional
Section: non-free/misc
Maintainer: Alexander V. Gusev <maintainers@astralinux.ru>
Installed-Size: 4082
Filename: pool/non-free/t/trnet-firmware/trnet-firmware_1.2.3_all.deb
Size: 1607072
MD5sum: 1cca9efcba5e4f297ae2fd3c7cdf42e8
SHA1: e30d114184057894cb1502faf05a7d7332e4980e
SHA256: 45f07f547dd0e09149875cb19f77c4825e96df6389ace9e0aed7779f85962eb0
Description: Firmware for trnet drivers
 This package provides firmware used by trnet drivers.

Package: unrar
Architecture: amd64
Version: 1:6.2.6-1+deb12u1.astra1
Priority: optional
Section: non-free/utils
Source: unrar-nonfree
Maintainer: UnRar maintainer team <team+unrar-nonfree@tracker.debian.org>
Installed-Size: 337
Depends: libc6 (>= 2.34), libgcc-s1 (>= 3.3.1), libstdc++6 (>= 11)
Filename: pool/non-free/u/unrar-nonfree/unrar_6.2.6-1+deb12u1.astra1_amd64.deb
Size: 141476
MD5sum: f02319d74504afe6b8c3b9ac2eccf5e8
SHA1: 80aabceda1dbe5b76e93a1eaba2033648dd44d58
SHA256: 48b6f7afcb2457c38453aa13a618b7741174eefb82416ca4c98710a2db2fb004
Homepage: https://www.rarlab.com/
Description: Unarchiver for .rar files (non-free version)
 Unrar can extract files from .rar archives. If you want to create .rar
 archives, install package rar.
Unsigned-SHA1: 406b5aa0154e90b835e924fb386f219f0cb62989

Package: amd64-microcode
Architecture: amd64
Version: 3.20250311.1
Priority: standard
Section: non-free-firmware/admin
Maintainer: Henrique de Moraes Holschuh <hmh@debian.org>
Installed-Size: 698
Recommends: initramfs-tools (>= 0.113~) | dracut (>= 044) | tiny-initramfs
Breaks: intel-microcode (<< 2)
Filename: pool/non-free-firmware/a/amd64-microcode/amd64-microcode_3.20250311.1_amd64.deb
Size: 277968
MD5sum: 8f83de0744b94f8e69739ae8bb4bc05d
SHA1: 23784aca62b8a02ef648984e83a979361029e8eb
SHA256: ab8f217e34d8f4fbd701c7ff379f0d00502738d7bda1460cea9dbdc113b0c177
Description: Platform firmware and microcode for AMD CPUs and SoCs
 This package contains microcode patches for AMD AMD64
 processors.  AMD releases microcode patches to correct
 processor behavior as documented in the respective processor
 revision guides.
 .
 This package includes the required firmware to enable AMD
 SEV (Secure Encrypted Virtualization) functionality.
 .
 This package also includes AMD TAs (Trusted Applications)
 required by AMD platform drivers such as AMD PMF (Platform
 Management Framework).
 .
 For Intel processors, please refer to the intel-microcode package.

Package: intel-microcode
Architecture: amd64
Version: 3.20250812.1.astra1
Priority: standard
Section: non-free-firmware/admin
Maintainer: Henrique de Moraes Holschuh <hmh@debian.org>
Installed-Size: 19297
Depends: iucode-tool (>= 1.0)
Recommends: initramfs-tools (>= 0.113~)
Conflicts: microcode.ctl (<< 0.18~0)
Filename: pool/non-free-firmware/i/intel-microcode/intel-microcode_3.20250812.1.astra1_amd64.deb
Size: 11550632
MD5sum: 2cef2dbec391892b696cbd241ea8b99f
SHA1: 926d94ea9a5ef138714110ed15abf61428e4b4cb
SHA256: 4e7b876be038d3e0324616e26e24896969e4df1dab038918920d7e3f0bc83221
Homepage: https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files
Description: Processor microcode firmware for Intel CPUs
 This package contains updated system processor microcode for
 Intel i686 and Intel X86-64 processors.  Intel releases microcode
 updates to correct processor behavior as documented in the
 respective processor specification updates.
 .
 For AMD processors, please refer to the amd64-microcode package.

