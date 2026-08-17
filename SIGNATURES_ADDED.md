# Extended detection signatures

Added/expanded fingerprints for:

- gtest / GoogleTest
- cereal
- cppzmq
- dmlc-core
- rabit
- Jansson (`libjansson4`, plus `libjasson4` typo alias)
- XGBoost R binding (`R-package`)
- libfpta / `libfpta_utils`
- Zeek Broker / `libbroker`
- `libpcom` / `libpcomn` (conservative because upstream identity is ambiguous)
- p0f
- POCO
- pypcap (`python-pycap` alias)
- rabbitmq-c
- firmware-bnx2x (`firmaware-bnx2x` typo alias)
- Zeek / Bro

The scanner also now uses file-name and file-path evidence during directory scans, in addition to ELF DT_NEEDED, dynamic symbols, strings and source contents.

Notes:
- `R-package` is treated as an XGBoost language binding/subcomponent, not automatically as a separate OSS dependency.
- `firmware-bnx2x` is classified as firmware, not as a normal userspace library.
- GoogleTest is normally a build/test dependency; verify whether test binaries are actually shipped before adding it to a production SBOM.
