sbom_astra_cve_working.py version: 2026-07-24-astra-v1
Script path: /home///distrib/sbom_astra_cve_working.py
Script sha256/16: a38a4392dc5b4115
Python: /home//venv/bin/python
CWD: /home//results/2026-08-07/
Mode: first generate SBOM with Syft, then scan SBOM against Astra Linux OVAL

=== STEP 1: Skip Syft ===
Using existing SBOM: /home//results/2026-08-07//sbom//deb.json

=== STEP 2: Read SBOM and classify components ===
Reading SBOM: /home//results/2026-08-07//sbom//deb.json
Debug JSONL: /home//results/2026-08-07//debug/distrib//astra_cve.classification.jsonl
Total components walked recursively: 370
deb components detected: 370
Astra deb components: 370
Other components: 0

Decision counts:
  DEB: 370

First deb examples:
  clickhouse-client 25.8.18.1 | src=clickhouse-client | purl=pkg:deb/clickhouse-client@25.8.18.1?arch=amd64
  clickhouse-common-static 25.8.18.1 | src=clickhouse-common-static | purl=pkg:deb/clickhouse-common-static@25.8.18.1?arch=amd64
  clickhouse-server 25.8.18.1 | src=clickhouse-server | purl=pkg:deb/clickhouse-server@25.8.18.1?arch=amd64
  conntrackd 1.4.7-1+b7 | src=conntrackd | purl=pkg:deb/conntrackd@1:1.4.7-1+b7?arch=amd64
  default-libmysqlclient-dev 1.1.0+b3 | src=default-libmysqlclient-dev | purl=pkg:deb/default-libmysqlclient-dev@1.1.0+b3?arch=amd64
  dpkg-dev 1.21.22.astra.se7 | src=dpkg-dev | purl=pkg:deb/dpkg-dev@1.21.22.astra.se7?arch=all
  flog 1.8+orig-2 | src=flog | purl=pkg:deb/flog@1.8+orig-2?arch=amd64
  galera-3 25.3.37-1+b7 | src=galera-3 | purl=pkg:deb/galera-3@25.3.37-1+b7?arch=amd64
  gdb 13.1-3+b7 | src=gdb | purl=pkg:deb/gdb@13.1-3+b7?arch=amd64
  google-chrome-stable 150.0.7871.46-1 | src=google-chrome-stable | purl=pkg:deb/google-chrome-stable@150.0.7871.46-1?arch=amd64

=== STEP 3a: Discover Astra OVAL files ===
[discovery] total OVAL files found: 5
[discovery]   https://download.astralinux.ru/artifactory/al-oval/1.7_x86-64/oval-definitions-alse-1.7.xml
[discovery]   https://download.astralinux.ru/artifactory/al-oval/1.8_x86-64/oval-definitions-alse-1.8.xml
[discovery]   https://download.astralinux.ru/artifactory/al-oval/3.8_s390x/oval-definitions-alse-3.8.xml
[discovery]   https://download.astralinux.ru/artifactory/al-oval/4.7_arm/oval-definitions-alse-4.7.xml
[discovery]   https://download.astralinux.ru/artifactory/al-oval/4.8_arm/oval-definitions-alse-4.8.xml
[discovery] cached discovered URL list (5 files): /home//.cache/astra_oval/discovered_urls.json

=== STEP 3b: Download/cache Astra OVAL files ===
[oval] from cache (13h): https://download.astralinux.ru/artifactory/al-oval/1.7_x86-64/oval-definitions-alse-1.7.xml
[oval] from cache (13h): https://download.astralinux.ru/artifactory/al-oval/1.8_x86-64/oval-definitions-alse-1.8.xml
[oval] from cache (13h): https://download.astralinux.ru/artifactory/al-oval/3.8_s390x/oval-definitions-alse-3.8.xml
[oval] from cache (13h): https://download.astralinux.ru/artifactory/al-oval/4.7_arm/oval-definitions-alse-4.7.xml
[oval] from cache (13h): https://download.astralinux.ru/artifactory/al-oval/4.8_arm/oval-definitions-alse-4.8.xml

=== STEP 4: Parse OVAL ===
[oval-parse] entries parsed: 0
[oval-parse] WARN: 0 entries and no definition with class="patch" found at all — definitions present: ['vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability']
[oval-parse] entries parsed: 0
[oval-parse] WARN: 0 entries and no definition with class="patch" found at all — definitions present: ['vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability']
[oval-parse] entries parsed: 0
[oval-parse] WARN: 0 entries and no definition with class="patch" found at all — definitions present: ['vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability']
[oval-parse] entries parsed: 0
[oval-parse] WARN: 0 entries and no definition with class="patch" found at all — definitions present: ['vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability']
[oval-parse] entries parsed: 0
[oval-parse] WARN: 0 entries and no definition with class="patch" found at all — definitions present: ['vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability', 'vulnerability']

WARNING: No OVAL entries parsed from any Astra OVAL file — writing report with 0 CVE matches (see [oval-parse] WARN above for the actual cause)

=== STEP 7: Export XLSX ===
Excel saved: /home//results/2026-08-07//reports//cve_report_astra.xlsx
Findings sidecar saved: /home//results/2026-08-07//reports//cve_report_astra.xlsx.findings.json
[scan-full] <<< step 'astra-cve' finished at 2026-08-07 14:32:59 — took 10.3s (0.2 min)
