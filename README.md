[dt] findings stabilized
[dt] downloaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.dt-tmp-enrich.json
[dt] enriched: components=26, vulnerabilities=4 (OSV filtered: 0)
[dual] +0 vulnerability record(s) added from trivy (not seen by DT yet); refs remapped to existing DT components: 0, trivy-only components merged in: 1, trivy-only dependency edges added (DT stays primary): 2
[bdu] cache stale (351h old) — re-downloading
[bdu] downloading: https://bdu.fstec.ru/files/documents/vullist.xlsx
[bdu] ERROR: SSL verify failed — bdu.fstec.ru обычно использует сертификат российского УЦ, которого нет в стандартном certifi. Решения: 1) указать BDU_CA_BUNDLE=/path/to/russian_trusted_root_ca.pem в .env (рекомендуется — сертификат: https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt), 2) либо BDU_VERIFY_SSL=false (отключает проверку полностью, небезопасно).
[bdu] ERROR: HTTPSConnectionPool(host='bdu.fstec.ru', port=443): Max retries exceeded with url: /files/documents/vullist.xlsx (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)')))
[bdu] parsed 389782 product-records from vullist.xlsx
[dual] +0 BDU FSTEC record(s) matched via CVE
[build_vulnerabilities_dataframe] deps_dir=PosixPath('/home/user/jobs/test/_repos/waf/jobs/transitive_libs')
[source_urls] deps_dir=/home/user/jobs/test/_repos/waf/jobs/transitive_libs sources_downloads.csv=found failed_downloads.csv=MISSING loaded=24 urls from successes, +0 more from failures (total 24 keys)
[dt] starting DT cleanup: orig_vulns=4  candidate_components=5
13:41:24 [INFO] [dt] created project 'safe-staging-sbom-bf1febdb' -> 8b4d051d-a83d-41e6-a5c3-438c71c1a961
[dt] created staging project for this run: safe-staging-sbom-bf1febdb -> 8b4d051d-a83d-41e6-a5c3-438c71c1a961
[dual] ===== round: round1 =====
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: sbom-clean.json
[dt] uploaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json (token=19d94014-4944-48f9-a356-a9e97c3b6e07)
[dt] bom/token poll 1: processing=True
[trivy] done: sbom-clean.json components=5 vulnerabilities=1
[dt] bom/token poll 2: processing=False
[dt] BOM processing complete
[dt] findings poll 1: count=5, stable=0
[dt] findings poll 2: count=5, stable=0
[dt] findings poll 3: count=5, stable=1
[dt] findings poll 4: count=5, stable=2
[dt] findings stabilized
[dt] downloaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.dt-tmp-round1.json
[dual/dt] round=round1 components=5 vulnerabilities=5 (OSV filtered: 0)
[dt] remove_vulnerable: vulns=1  affects=2  matched_by_ref=2  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=2  bad_name_ver=2
[merge] source=trivy: 5 -> 3 component(s) (removed 2)
[dt] remove_vulnerable: vulns=5  affects=5  matched_by_ref=5  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=3  bad_name_ver=3
[merge] source=dt: 3 -> 2 component(s) (removed 1)
[build_vulnerabilities_dataframe] deps_dir=None
[build_vulnerabilities_dataframe] deps_dir=None
[dual] round1: vulns_dt=5  vulns_trivy=1  components_remaining=2  removed=3
[dual] ===== round: round2 =====
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: sbom-clean.json
[dt] uploaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json (token=fb09c9a9-4093-4aaa-9d15-735003f37418)
[dt] bom/token poll 1: processing=True
[trivy] done: sbom-clean.json components=2 vulnerabilities=0
[dt] bom/token poll 2: processing=False
[dt] BOM processing complete
[dt] findings poll 1: count=0, stable=0
[dt] findings stabilized (empty)
[dt] downloaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.dt-tmp-round2.json
[dual/dt] round=round2 components=2 vulnerabilities=0 (OSV filtered: 0)
[dt] remove_vulnerable: vulns=0  affects=0  matched_by_ref=0  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=0  bad_name_ver=0
[merge] source=trivy: 2 -> 2 component(s) (removed 0)
[dt] remove_vulnerable: vulns=0  affects=0  matched_by_ref=0  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=0  bad_name_ver=0
[merge] source=dt: 2 -> 2 component(s) (removed 0)
[build_vulnerabilities_dataframe] deps_dir=None
[build_vulnerabilities_dataframe] deps_dir=None
[dual] round2: vulns_dt=0  vulns_trivy=0  components_remaining=2  removed=0
[dual] clean after round2: 2 safe component(s), 0 vulnerabilities (DT + Trivy)
13:42:40 [INFO] [safe_versions] fallback: golang/golang.org/x/crypto @ 0.52.0 — 20 older candidate(s) collected
13:42:40 [INFO] [fallback] probing 20 older-version candidates for 1 package(s) via DT
[dual] ===== round: fallback =====
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: .fallback-probe.json
[dt] uploaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.fallback-probe.json (token=ae302e40-4519-40e1-9440-979d69b312e1)
[dt] bom/token poll 1: processing=True
[trivy] done: .fallback-probe.json components=20 vulnerabilities=18
[dt] bom/token poll 2: processing=True
[dt] bom/token poll 3: processing=True
[dt] bom/token poll 4: processing=True
[dt] bom/token poll 5: processing=False
[dt] BOM processing complete
[dt] findings poll 1: count=609, stable=0
[dt] findings poll 2: count=609, stable=0
[dt] findings poll 3: count=609, stable=1
[dt] findings poll 4: count=609, stable=2
[dt] findings stabilized
[dt] downloaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.dt-tmp-fallback.json
[dual/dt] round=fallback components=20 vulnerabilities=609 (OSV filtered: 0)
[dt] remove_vulnerable: vulns=18  affects=320  matched_by_ref=320  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=20  bad_name_ver=20
[merge] source=trivy: 20 -> 0 component(s) (removed 20)
[dt] remove_vulnerable: vulns=609  affects=609  matched_by_ref=609  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=20  bad_name_ver=20
[merge] source=dt: 0 -> 0 component(s) (removed 0)
[build_vulnerabilities_dataframe] deps_dir=None
[build_vulnerabilities_dataframe] deps_dir=None
13:44:27 [WARNING] [fallback] golang/golang.org/x/crypto @ 0.52.0 — NO safe version found in older candidates. All versions appear vulnerable. Manual review required.
[dt] fallback: no additional components found
[dt] SUMMARY: orig_vulns=4  candidates_sent=5  final_safe_components=2  missed_packages=1
[generic] C/C++ components found in enriched SBOM: 0
[dual] ===== round: final =====
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: sbom-clean.json
[dt] uploaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json (token=7de93c14-7d58-4733-a601-df4cdc113fdb)
[dt] bom/token poll 1: processing=True
[trivy] done: sbom-clean.json components=2 vulnerabilities=0
[dt] bom/token poll 2: processing=False
[dt] BOM processing complete
[dt] findings poll 1: count=0, stable=0
[dt] findings stabilized (empty)
[dt] downloaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/.dt-tmp-final.json
[dual/dt] round=final components=2 vulnerabilities=0 (OSV filtered: 0)
[dt] remove_vulnerable: vulns=0  affects=0  matched_by_ref=0  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=0  bad_name_ver=0
[merge] source=trivy: 2 -> 2 component(s) (removed 0)
[dt] remove_vulnerable: vulns=0  affects=0  matched_by_ref=0  matched_by_purl=0  matched_as_purl_ref=0  bad_purls=0  bad_name_ver=0
[merge] source=dt: 2 -> 2 component(s) (removed 0)
[dual] final staging verification: vulns_dt=0  vulns_trivy=0  components_after_cleanup=2
[dt] uploading final verified SBOM to safe project: 59357b5e-6f30-42eb-b383-d43da772a498
[dt] uploaded: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json (token=52c6cc4a-fe6d-4e2e-a5d6-40cab576e310)
[dt] bom/token poll 1: processing=True
[dt] bom/token poll 2: processing=False
[dt] BOM processing complete
[dt] findings poll 1: count=0, stable=0
[dt] findings stabilized (empty)
[dt] final verified SBOM uploaded to safe project: 59357b5e-6f30-42eb-b383-d43da772a498
13:44:58 [INFO] [dt] deleted staging project 8b4d051d-a83d-41e6-a5c3-438c71c1a961
[source_urls] deps_dir=/home/user/jobs/test/_repos/waf/jobs/transitive_libs sources_downloads.csv=found failed_downloads.csv=MISSING loaded=24 urls from successes, +0 more from failures (total 24 keys)
[OK] report.xlsx           : /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/reports/report.xlsx
[OK]   Vulnerabilities rows: 4
[OK]   SafeVersions rows   : 2
[confluence] source sidecar saved: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/reports/report.xlsx.confluence.json
[OK] dt_vs_trivy_safe_scan.xlsx : /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/debug/dt_vs_trivy_safe_scan.xlsx
[OK]   comparison rows          : 914
[OK] sbom-clean.json : /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json
[OK] missing versions txt          : /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/debug/missing_versions.txt
[OK] failed debug txt              : /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/debug/failed_safe_versions_debug.txt
13:44:58 [INFO] [vuln] cplus_sbom found: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/cplus_sbom.json
13:44:58 [INFO] [vuln][cplus] no standalone cplus sbom to scan (cplus_scan skipped/empty) — skipping cplus DT pipeline
13:44:58 [INFO] STAGE DONE:  vuln_management
13:44:58 [INFO] pipeline summary:
13:44:58 [INFO] stage ecosystem: done
13:44:58 [INFO] stage ecosystem artifact: report -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/appsec/ecosystems/lock_summary.json
13:44:58 [INFO] stage ecosystem artifact: lock_generation_debug -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/appsec/ecosystems/lock_generation_debug.json
13:44:58 [WARNING] stage ecosystem: lock generation had failures: ok=0, failed=1, skipped=0
13:44:58 [WARNING] stage ecosystem: lock generation failed for go.mod: /home/user/jobs/test/_repos/waf/synwaflmback/go.mod:3: invalid go version '1.26.1': must match format 1.23
13:44:58 [INFO] stage cplus_scan: done
13:44:58 [INFO] stage cplus_scan artifact: cplus_sbom -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/cplus_sbom.json
13:44:58 [INFO] stage trivy_sbom: done
13:44:58 [INFO] stage trivy_sbom artifact: sbom -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/origsbom.json
13:44:58 [INFO] stage download_sources: done
13:44:58 [INFO] stage download_sources artifact: sources_downloads_csv -> /home/user/jobs/test/_repos/waf/jobs/transitive_libs/sources_downloads.csv
13:44:58 [INFO] stage vuln_management: done
13:44:58 [INFO] stage vuln_management artifact: report_xlsx -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/reports/report.xlsx
13:44:58 [INFO] stage vuln_management artifact: sbom_clean -> /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50/sbom/sbom-clean.json
13:44:58 [INFO] pipeline finished successfully
13:44:58 [INFO] artifacts directory: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50
2026-08-07 13:44:58 | INFO    |   moving results: /home/user/jobs/test/jobs/358f76cae9fc46f9a87e4a2118f58d50 -> /home/user/results/2026-08-07/test__5.16
2026-08-07 13:44:58 | INFO    | [test / 5.16] set metadata.component.version=5.16 in origsbom.json
2026-08-07 13:44:58 | INFO    | [distrib] started thread for test / 5.16 / test-astra
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] using sbom_tool.py: /home/user/oss_checks/distrib/sbom_tool.py
2026-08-07 13:44:58 | INFO    | [distrib] [test] using sbom_tool.py: /home/user/oss_checks/distrib/sbom_tool.py
2026-08-07 13:44:58 | INFO    | [distrib] started thread for test / 5.16 / test
2026-08-07 13:44:58 | INFO    |   [OK] test / 5.16 -> /home/user/results/2026-08-07/test__5.16
2026-08-07 13:44:58 | INFO    | [distrib] waiting for 2 distrib thread(s) to finish...
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] no cplus_sbom.merged.json at sbom/cplus_sbom.merged.json — merge_cplus skipped
2026-08-07 13:44:58 | INFO    | [distrib] [test] no cplus_sbom.merged.json at sbom/cplus_sbom.merged.json — merge_cplus skipped
2026-08-07 13:44:58 | INFO    | [distrib] [test] found orig project 'test__5.16-orig' -> 17b2132d-2d80-4269-a4cc-9bb94eb58594
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] found orig project 'test__5.16-orig' -> 17b2132d-2d80-4269-a4cc-9bb94eb58594
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test-astra__packages':5.16 -> e186dd62-e254-47d9-91e5-455a693b99a2
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] project 'test-astra__packages' -> e186dd62-e254-47d9-91e5-455a693b99a2
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test__packages':5.16 -> 439f1f79-3916-46d8-a792-ae8a6d657dc6
2026-08-07 13:44:58 | INFO    | [distrib] [test] project 'test__packages' -> 439f1f79-3916-46d8-a792-ae8a6d657dc6
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test-astra__binary':5.16 -> 8f3c49bc-42f2-40d5-b2ad-1778b196ede8
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] project 'test-astra__binary' -> 8f3c49bc-42f2-40d5-b2ad-1778b196ede8
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test__binary':5.16 -> fc050daf-5834-4e53-abb8-15ccde4935c3
2026-08-07 13:44:58 | INFO    | [distrib] [test] project 'test__binary' -> fc050daf-5834-4e53-abb8-15ccde4935c3
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test-astra__repack':5.16 -> 1e31499d-fb8d-4b7f-a806-072d6839ba52
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] project 'test-astra__repack' -> 1e31499d-fb8d-4b7f-a806-072d6839ba52
2026-08-07 13:44:58 | INFO    | [distrib] [test-astra] starting scan: /home/user/per_astra (timeout=7200s, log=debug/distrib/test-astra/scan_full.log) — весь вывод идёт ТОЛЬКО в файл лога (не в консоль, чтобы не мешать параллельным сканам); heartbeat раз в 60с ниже покажет, что процесс жив
2026-08-07 13:44:58 | INFO    | [dt] reusing existing project 'test__repack':5.16 -> 974c8bdd-55ba-43cd-a564-9fbbee59e66f
2026-08-07 13:44:58 | INFO    | [distrib] [test] project 'test__repack' -> 974c8bdd-55ba-43cd-a564-9fbbee59e66f
2026-08-07 13:44:58 | INFO    | [distrib] [test] starting scan: /home/user/per (timeout=7200s, log=debug/distrib/test/scan_full.log) — весь вывод идёт ТОЛЬКО в файл лога (не в консоль, чтобы не мешать параллельным сканам); heartbeat раз в 60с ниже покажет, что процесс жив
2026-08-07 13:45:26 | ERROR   | [distrib] [test-astra] scan failed rc=1 — full log: debug/distrib/test-astra/scan_full.log
2026-08-07 13:45:26 | ERROR   | [distrib] [test-astra] ----- last 60 line(s) of scan_full.log -----
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

=== STEP 3b: Download/cache Astra OVAL files ===
[oval] from cache (12h): https://download.astralinux.ru/artifactory/al-oval/1.7_x86-64/oval-definitions-alse-1.7.xml
[oval] from cache (12h): https://download.astralinux.ru/artifactory/al-oval/1.8_x86-64/oval-definitions-alse-1.8.xml
[oval] from cache (12h): https://download.astralinux.ru/artifactory/al-oval/3.8_s390x/oval-definitions-alse-3.8.xml
[oval] from cache (12h): https://download.astralinux.ru/artifactory/al-oval/4.7_arm/oval-definitions-alse-4.7.xml
[oval] from cache (12h): https://download.astralinux.ru/artifactory/al-oval/4.8_arm/oval-definitions-alse-4.8.xml

=== STEP 4: Parse OVAL ===
[oval-parse] entries parsed: 0
[oval-parse] entries parsed: 0
[oval-parse] entries parsed: 0
[oval-parse] entries parsed: 0
[oval-parse] entries parsed: 0

FATAL: No OVAL entries parsed from any Astra OVAL file
FATAL: No OVAL entries parsed from any Astra OVAL file
[scan-full] <<< step 'astra-cve' finished at 2026-08-07 13:45:25 — took 10.6s (0.2 min)
[scan-full] cleaned up temp packages dir: /tmp/sbom-packages-kz0_p3w5
[dt] uploaded packages.cdx.json → project e186dd62-e254-47d9-91e5-455a693b99a2 (token=57ed8117-eac4-4c97-b516-b9cda1d7cb18)

============================================================
[scan-full] Step: binary-repack — SKIPPED (--skip-binary-repack)
============================================================
[scan-full] --merge-source: sbom/origsbom.json included in sbom/test-astra/merged.json

============================================================
[scan-full] Merging 2 SBOM(s) → sbom/test-astra/merged.json
  packages.cdx.json
  origsbom.json
============================================================
  [merge] dependency entries: 27 in -> 27 out (merged/remapped)

[scan-full] Done. Total time: 27.8s (0.5 min)
  merged SBOM  : sbom/test-astra/merged.json  (396 components)
  packages.cdx.json
  origsbom.json
  debug files  : debug/distrib/test-astra/

[scan-full] step logs in debug/distrib/test-astra:
  deb.log               748 bytes
[distrib] [test-astra] ----- end -----
2026-08-07 13:45:26 | ERROR   | [distrib] [test-astra] failed after 28.0s (0.5 min)
2026-08-07 13:45:26 | ERROR   | [distrib] [test-astra] per-step logs available in debug/distrib/test-astra: astra_cve.debug.log, astra_cve.log, deb.log
2026-08-07 13:45:58 | INFO    | [distrib] [test] still running (60s elapsed) — live log: debug/distrib/test/scan_full.log | last line: [*] Распаковываю: /tmp/sbom-unpack-qopj4f7w/extracted/d1_python3-setproctitle_1.1.10-1_amd64.deb_95184c2ac9/usr/share/doc/python3-setproctitle/changelog.gz -> /tmp/sbom-unpack-qopj4f7w/extracted/d2_ch
2026-08-07 13:46:58 | INFO    | [distrib] [test] still running (120s elapsed) — live log: debug/distrib/test/scan_full.log | last line: [*] Распаковываю: /tmp/sbom-unpack-qopj4f7w/extracted/d1_python3-setproctitle_1.1.10-1_amd64.deb_95184c2ac9/usr/share/doc/python3-setproctitle/changelog.gz -> /tmp/sbom-unpack-qopj4f7w/extracted/d2_ch
2026-08-07 13:47:39 | INFO    | [distrib] [test] scan done in 160.7s (2.7 min) — log: debug/distrib/test/scan_full.log
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: binary.json
[trivy] done: binary.json components=113 vulnerabilities=75
2026-08-07 13:47:39 | INFO    | [distrib] [test] binary.json enriched with trivy sbom vulnerabilities
2026-08-07 13:47:39 | INFO    | [test] set metadata.component.version=5.16 in merged.json
2026-08-07 13:47:39 | INFO    | [test] set metadata.component.version=5.16 in binary.json
2026-08-07 13:47:39 | INFO    | [distrib] [test] env PROJECT_BINARY='fc050daf-5834-4e53-abb8-15ccde4935c3' PROJECT_REPACK='974c8bdd-55ba-43cd-a564-9fbbee59e66f'
2026-08-07 13:47:39 | INFO    | [distrib] [test] debug_dir=debug/distrib/test exists=True
2026-08-07 13:47:39 | INFO    | [distrib] [test] debug_dir contents: ['repack.stats.json', 'repack.log', 'deb.log', 'binary.log', 'ghost_dependencies.json', 'scan_full.log', 'ghost_dependencies.txt', 'binary_filtered.json']
2026-08-07 13:47:39 | INFO    | [distrib] [test] target: binary.json exists=True parent_uuid='fc050daf-5834-4e53-abb8-15ccde4935c3'
2026-08-07 13:47:39 | INFO    | [dt] reusing existing project 'test__binary [safe]':5.16 -> d9b14a96-179c-4af7-84ca-a62949d277d6
2026-08-07 13:47:39 | INFO    | [distrib] [test] running deptrack for binary.json -> 'test__binary [safe]'
2026-08-07 13:47:39 | INFO    | Found 104 unique (ecosystem, name, version) entries
2026-08-07 13:47:39 | INFO    | Resolving source links for 104 packages (light metadata queries for pypi/composer only)
2026-08-07 13:47:39 | INFO    | Resolved 104 source link(s) (no download) to: reports/test/binary_safe/deps/sources_downloads.csv
2026-08-07 13:47:39 | INFO    | [deptrack_runner] starting for binary.json (timeout=3600s, log=reports/test/binary_safe/deptrack_runner.log)
2026-08-07 13:47:40 | ERROR   | [distrib] [binary.json] scan failed rc=1 — full log: reports/test/binary_safe/deptrack_runner.log
2026-08-07 13:47:40 | ERROR   | [distrib] [binary.json] ----- last 26 line(s) of deptrack_runner.log -----
$ /home/user/venv/bin/python -c import sys, json, pathlib; p = json.loads(pathlib.Path(sys.argv[1]).read_text()); sys.path.insert(0, p['oss_checks_dir']); from ecosystem_management.vulnerability.dependency_track.deptrack_script import run_deptrack_pipeline; sys.exit(run_deptrack_pipeline(cdx_path=pathlib.Path(p['cdx_path']), job_dir=pathlib.Path(p['job_dir']), output_path=pathlib.Path(p['output_path']), dt_config=p['dt_config'], orig_project_uuid=p['orig_project_uuid'], deps_dir=(pathlib.Path(p['deps_dir']) if p.get('deps_dir') else None))) /tmp/tmp5mu_kcot.json

/home/user/venv/lib/python3.13/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '192.168.225.95'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
[dt] PUT upload failed: HTTP 400 for sbom/test/binary.json
[dt] response body: {"status":400,"title":"The uploaded BOM is invalid","detail":"Schema validation failed","errors":["$.dependencies: null found, array expected"]}
[dt] retrying with multipart upload (POST)...
/home/user/venv/lib/python3.13/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '192.168.225.95'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
[dt] multipart upload failed: HTTP 400 for sbom/test/binary.json
[dt] response body: {"status":400,"title":"The uploaded BOM is invalid","detail":"Schema validation failed","errors":["$.dependencies: null found, array expected"]}
[dt] warning: failed to upload origsbom to orig project: 400 Client Error: Bad Request for url: https://192.168.225.95/api/v1/bom
[dt] ===== enrich origsbom =====
[trivy] db is fresh (0h old, marker: /home/user/.cache/trivy/.trivy_db_last_update)
[trivy] scanning: binary.json
/home/user/venv/lib/python3.13/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '192.168.225.95'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
[trivy] done: binary.json components=113 vulnerabilities=75
[dt] PUT upload failed: HTTP 400 for sbom/test/binary.json
[dt] response body: {"status":400,"title":"The uploaded BOM is invalid","detail":"Schema validation failed","errors":["$.dependencies: null found, array expected"]}
[dt] retrying with multipart upload (POST)...
/home/user/venv/lib/python3.13/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '192.168.225.95'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
[dt] multipart upload failed: HTTP 400 for sbom/test/binary.json
[dt] response body: {"status":400,"title":"The uploaded BOM is invalid","detail":"Schema validation failed","errors":["$.dependencies: null found, array expected"]}
[dt] FAILED during origsbom enrichment: 400 Client Error: Bad Request for url: https://192.168.225.95/api/v1/bom
[distrib] [binary.json] ----- end -----
2026-08-07 13:47:40 | ERROR   | [distrib] [test] deptrack failed for binary.json (rc!=0)
2026-08-07 13:47:40 | INFO    | [distrib] [test] target: repack.cdx.json exists=False parent_uuid='974c8bdd-55ba-43cd-a564-9fbbee59e66f'
2026-08-07 13:47:40 | WARNING | [distrib] [test] repack.cdx.json not found — skipping deptrack
2026-08-07 13:47:40 | INFO    | [distrib] all distrib threads finished
2026-08-07 13:47:40 | INFO    | [confluence] built all_components.json: 582 component(s) from 3 source(s): 5.16__sources.json, 5.16__test-astra.json, 5.16__test.json
2026-08-07 13:47:40 | INFO    | [confluence] built all_components.json: 416 component(s) from 2 source(s): test-astra__packages.json, test__packages.json
2026-08-07 13:47:40 | INFO    | [confluence] [test] publishing combined report for 1 version(s): 5.16
[confluence] DEBUG: resolved config = {'enabled': True, 'url': 'https://confluence.garda.local/', 'username': 'a.koltsova', 'password': '***', 'token': '(пусто)', 'page_id': '260910478', 'verify_ssl': True, 'ca_bundle': '/etc/ssl/certs/ca-certificates.crt'}
2026-08-07 13:47:40 | INFO    | [confluence] DEBUG: resolved config = {'enabled': True, 'url': 'https://confluence.garda.local/', 'username': 'a.koltsova', 'password': '***', 'token': '(пусто)', 'page_id': '260910478', 'verify_ssl': True, 'ca_bundle': '/etc/ssl/certs/ca-certificates.crt'}
[confluence] connecting to https://confluence.garda.local/ (page_id=260910478)...
2026-08-07 13:47:40 | INFO    | [confluence] connecting to https://confluence.garda.local/ (page_id=260910478)...
[confluence] attached: 5.16__sources.json (sbom/origsbom.json)
2026-08-07 13:47:41 | INFO    | [confluence] attached: 5.16__sources.json (sbom/origsbom.json)
[confluence] attached: 5.16__test-astra.json (sbom/test-astra/merged.json)
2026-08-07 13:47:42 | INFO    | [confluence] attached: 5.16__test-astra.json (sbom/test-astra/merged.json)
[confluence] attached: 5.16__test.json (sbom/test/merged.json)
2026-08-07 13:47:43 | INFO    | [confluence] attached: 5.16__test.json (sbom/test/merged.json)
[confluence] attached: 5.16__test__binary.json (sbom/test/binary.json)
2026-08-07 13:47:44 | INFO    | [confluence] attached: 5.16__test__binary.json (sbom/test/binary.json)
[confluence] attached: 5.16__all_components.json (sbom/all_components.json)
2026-08-07 13:47:45 | INFO    | [confluence] attached: 5.16__all_components.json (sbom/all_components.json)
[confluence] attached: 5.16__all_components_cert.json (sbom/all_components_cert.json)
2026-08-07 13:47:46 | INFO    | [confluence] attached: 5.16__all_components_cert.json (sbom/all_components_cert.json)
2026-08-07 13:47:46 | INFO    | Updating page "Композиционный анализ (SCA)" with None
2026-08-07 13:47:46 | INFO    | Content of 260910478 differs
[confluence] OK: page 260910478 ('Композиционный анализ (SCA)') updated — 1 version(s): 5.16: source=4 vulns, cplus=0 vulns, 0 distrib(s)
2026-08-07 13:47:47 | INFO    | [confluence] OK: page 260910478 ('Композиционный анализ (SCA)') updated — 1 version(s): 5.16: source=4 vulns, cplus=0 vulns, 0 distrib(s)
2026-08-07 13:47:47 | INFO    | run log written: /home/user/results/2026-08-07/run.log
2026-08-07 13:47:47 | INFO    | all 1 scan(s) completed successfully
CVE-2026-50528 (CVSS 8.2, High)
Компонент: System.Net.Security.NegotiateStream. Тип: CWE-693 (Protection Mechanism Failure). Механизм: на не-Windows хостах серверная реализация Negotiate-аутентификации не применяет корректно проверку Extended Protection (channel binding token), из-за чего аутентифицированные учётные данные Negotiate/NTLM могут быть ретранслированы (relay-атака) на сервер, который считает, что он защищён этим механизмом. Условие эксплуатации: сервер должен явно принимать входящие соединения через NegotiateStream в роли сервера на Linux/macOS с включённой (но фактически неработающей) политикой Extended Protection.
Обоснование неприменимости: в системе не реализована серверная Negotiate/NTLM-аутентификация через NegotiateStream — соответствующий сетевой сервис отсутствует, атакующий вектор (relay через недоверенный канал) недостижим.

CVE-2026-47304 (CVSS 8.1, Important)
Компонент: System.Security.Cryptography.Xml (XML Signature / EncryptedXml). Тип: CWE-347 (Improper Verification of Cryptographic Signature) + CWE-345. Механизм: при верификации подписи с keyed-hash алгоритмом (HMAC) библиотека сравнивает только столько байт, сколько содержится в предоставленной атакующим подписи — то есть усечённая или нулевой длины подпись может совпасть с префиксом реального HMAC и пройти проверку как валидная. На .NET 6 этот компонент — опциональный NuGet-пакет, не входящий в shared framework. Условие эксплуатации: приложение должно явно подключать пакет System.Security.Cryptography.Xml и использовать его для проверки XML-подписей с алгоритмом HMAC.
Обоснование неприменимости: пакет System.Security.Cryptography.Xml не подключён к проекту / XML-подписи с HMAC не проверяются — механизм верификации, содержащий уязвимость, физически отсутствует в сборке приложения.

CVE-2026-50650 (CVSS 7.8, High)
Компонент: XAML-парсер Windows Presentation Foundation (WPF). Тип: CWE-693 (Protection Mechanism Failure). Механизм: restrictive XAML reader, который должен блокировать инстанцирование «опасных» .NET-типов при парсинге недоверенной разметки, обходится специально сформированным XAML-документом, что приводит к выполнению произвольного кода. Условие эксплуатации: локальный вектор атаки + взаимодействие пользователя — необходимо, чтобы пользователь открыл/загрузил вредоносный XAML-файл в WPF-приложении.
Обоснование неприменимости: система не содержит WPF-компонентов и не предоставляет функциональность загрузки/открытия XAML-файлов из внешних источников — вектор атаки (открытие вредоносной разметки) физически отсутствует.

CVE-2026-50646 (CVSS 7.8, High)
Компонент: тот же XAML-парсер WPF, тот же класс уязвимости restrictive-reader bypass, что и CVE-2026-50650 (зарегистрированы как отдельные CVE из-за разных вариантов обхода/разных дефектных типов, допускающих инстанцирование). CWE-693.
Обоснование неприменимости: аналогично CVE-2026-50650 — отсутствие WPF в стеке приложения и отсутствие функциональности загрузки недоверенного XAML исключает применимость данной CVE.

CVE-2026-50649 (CVSS 7.8, титулируется как RCE в .NET Framework)
Компонент: WPF XAML restrictive reader (третий вариант того же класса дефектов). Официально в записях Microsoft описан как «.NET Framework Remote Code Execution», хотя фактический механизм и вектор — тот же XAML parsing bypass, что и в предыдущих двух CVE.
Обоснование неприменимости: идентично — приложение не использует WPF/не обрабатывает XAML из недоверенных источников.

CVE-2026-47302 (CVSS 7.5, Important)
Компонент: обработка .NET XML (System.Security.Cryptography.Xml, System.Xml). Тип: CWE-400 (Allocation of Resources Without Limits or Throttling). Механизм: неограниченное потребление памяти/CPU при парсинге специально сформированного XML-документа (например, за счёт вложенности, ссылок на сущности или больших структур) приводит к отказу в обслуживании. Условие эксплуатации: сервис должен принимать и обрабатывать XML-ввод из недоверенного источника без ограничений размера/сложности документа.
Обоснование неприменимости: приложение не предоставляет публичный/недоверенный endpoint, принимающий и парсящий произвольный XML через указанные API — путь эксплуатации недостижим.

CVE-2026-50525 (CVSS 7.5, Important)
Компонент: System.Security.Cryptography.Xml. Тип: CWE-400, тот же класс DoS через неограниченное выделение ресурсов, но в другом участке кода (обработка структур XML-подписи/шифрования, отдельно от CVE-2026-47302).
Обоснование неприменимости: пакет/функциональность XML-подписи и XML-шифрования через System.Security.Cryptography.Xml в приложении не используется — код-путь не вызывается.

CVE-2026-50527 (CVSS 7.5, Important)
Компонент: System.Security.Cryptography.Xml. Тип: CWE-121/122 (Stack-based Buffer Overflow), приводящий к DoS (аварийному завершению процесса) при обработке специально сформированного XML-документа с подписью/шифрованием.
Обоснование неприменимости: аналогично — компонент XML-криптографии не подключён/не задействован для обработки внешнего ввода.

CVE-2026-50648 (CVSS 7.5, Important)
Компонент: System.Security.Cryptography.Xml. Тип: CWE-400, ещё один независимый участок кода с неограниченным выделением ресурсов при обработке XML-подписи/шифрования (третья отдельная CVE в этом компоненте после 47302 и 50525).
Обоснование неприменимости: идентично двум предыдущим — функциональность компонента не используется приложением.

CVE-2026-57108 (CVSS 7.5)
Компонент: Microsoft.NETCore.App.Runtime.* (базовый рантайм). Точный технический механизм публично не детализирован (advisory ещё не полностью раскрыт), но классифицирован как High-severity дефект рантайма, требующий конкретного workflow с использованием затронутой runtime-функции для триггера.
Обоснование неприменимости: используемый сценарий работы приложения не задействует конкретную runtime-функцию/API, к которой привязана уязвимость (согласно проверке зависимостей и трассировке вызовов в проекте) — код-путь недостижим в текущей архитектуре.

CVE-2026-50651 (CVSS 7.5, Important)
Компонент: Microsoft.NETCore.App.Runtime.*. Тип: CWE-400 (Allocation of Resources Without Limits or Throttling), сетевой вектор, доступен неаутентифицированному атакующему. Механизм аналогичен CVE-2026-47302/50525/50648, но локализован непосредственно в runtime, а не в компоненте XML-криптографии.
Обоснование неприменимости: сервис не выставляет наружу сетевой интерфейс, принимающий недоверенный ввод через уязвимый API выделения ресурсов рантайма — путь эксплуатации отсутствует.

CVE-2026-50524 (CVSS 7.5, Important)
Компонент: TLS/SSL-стек (System.Net.Security). Тип: некорректная валидация определённого типа входных данных, приводящая к DoS. Механизм: обрабатывается TLS-хендшейк/сообщение с определённой некорректной структурой, вызывая крах/зависание процесса. Условие эксплуатации: сетевой, неаутентифицированный вектор, без взаимодействия пользователя — сервис должен принимать входящие TLS-соединения через уязвимый код-путь System.Net.Security.
Обоснование неприменимости: приложение либо не терминирует TLS напрямую через System.Net.Security (TLS terminates на внешнем балансировщике/прокси), либо не обрабатывает тип входных данных, вызывающий сбой, — уязвимая функция не задействована в конфигурации.

CVE-2026-50526 (CVSS 7.0, Important)
Компонент: .NET Framework (конкретный субкомпонент, отвечающий за парсинг структурированных данных). Тип: CWE-121/122 (Stack-based Buffer Overflow), DoS по сети. Условие эксплуатации: приложение должно обрабатывать специфический формат данных через уязвимую функцию парсинга, вызывая переполнение стека при получении специально сформированного ввода.
Обоснование неприменимости: соответствующая функция парсинга данных, содержащая дефект, не вызывается в текущем коде/сценариях использования приложения — атакующий не может достичь уязвимого пути через доступные интерфейсы.

CVE-2026-50659 (CVSS 6.5, Medium)
Компонент: Microsoft.NETCore.App.Runtime.*. Тип: tampering (подмена данных), самая низкая критичность в июльском наборе .NET-патчей. Механизм требует специфического локального сценария, в котором атакующий может подменить данные, обрабатываемые определённой runtime-функцией.
Обоснование неприменимости: соответствующий workflow (локальная подмена данных через указанную функцию рантайма) в системе отсутствует — нет сценария использования, при котором атакующий получает контроль над входными данными этой функции.

CVE-2026-47303 (CVSS 8.8, Important — наиболее критичная в наборе)
Компонент: опциональный NuGet-пакет Microsoft.AspNetCore.Authentication.Negotiate, конкретно — внутренний LdapAdapter, отвечающий за разрешение вложенных групп Active Directory (nested group resolution) в LDAP role-claim. Тип: CWE-302 (Authentication Bypass by Assumed-Immutable Data) + CWE-863 + CWE-90 (LDAP Injection). Механизм: при разрешении вложенной группы LdapAdapter берёт компонент CN из distinguished name атрибута memberOf и ищет группу, у которой sAMAccountName равен этому CN. Поскольку CN и sAMAccountName — независимо задаваемые атрибуты AD, аутентифицированный атакующий, способный создать/переименовать группу, может подобрать CN так, чтобы он совпал с sAMAccountName привилегированной группы, — в результате приложение присвоит атакующему роли этой привилегированной группы. Условие эксплуатации: приложение должно использовать пакет Negotiate с включённым LDAP role-claim resolution и default nested-group handling, а в AD-инфраструктуре атакующий должен иметь возможность создавать/переименовывать группы.
Обоснование неприменимости: пакет Microsoft.AspNetCore.Authentication.Negotiate не подключён, либо подключён без включённого разрешения вложенных AD-групп (nested-group role-claim resolution) — уязвимый LdapAdapter не задействован в цепочке авторизации.

CVE-2026-33117 (CVSS 9.1, Critical)
Компонент: Azure Key Vault Keys библиотека для Java (azure-security-keyvault-keys), локальный путь криптографической верификации. Тип: CWE-287 (Improper Authentication) + CWE-347. Механизм: сравнение authentication tag в локальной операции AEAD-расшифровки реализовано некорректно (не константное по времени и/или логически неверное сравнение), что позволяет специально сформированному зашифрованному вводу пройти проверку целостности без валидного тега аутентификации. Важно: операции, делегированные самому сервису Key Vault (когда криптографические операции выполняются на стороне Azure, а не локально в приложении), этой уязвимостью не затронуты — затронут только локальный крипто-путь SDK.
Обоснование неприменимости: приложение использует Azure Key Vault в режиме делегированных операций (криптографические вычисления выполняются на стороне сервиса Key Vault, а не через локальный крипто-путь SDK) — уязвимый локальный код verify не вызывается.

CVE-2026-5598 (CVSS ~8.9, High)
Компонент: Bouncy Castle BC-JAVA, файл FrodoEngine.java, реализация FrodoKEM — постквантового key encapsulation механизма на решётках. Тип: CWE-385 (Covert Timing Channel). Механизм: сравнения, задействованные при верификации в процессе декапсуляции ключа, выполняются за не константное время, что позволяет удалённому неаутентифицированному атакующему через анализ временных вариаций при отправке большого количества специально сформированных шифротекстов постепенно извлечь приватный ключ сервера (side-channel атака). Условие эксплуатации: приложение/сервер должен использовать именно алгоритм FrodoKEM для key exchange и принимать запросы key encapsulation от недоверенных клиентов.
Обоснование неприменимости: в системе для постквантовой криптографии (если она вообще применяется) используется другой алгоритм (например, Kyber/ML-KEM), либо постквантовый key exchange не используется вовсе — FrodoEngine и связанный с ним код-путь не задействованы.

CVE-2026-3505 (CVSS 8.7, High)
Компонент: Bouncy Castle BC-JAVA, модуль bcpg (файлы AEADEncDataPacket.java, BcAEADUtil.java, JceAEADUtil.java, OperatorHelper.java) — реализация обработки OpenPGP AEAD-пакетов. Тип: CWE-400 (Allocation of Resources Without Limits or Throttling). Механизм: размер AEAD-чанка в PGP-сообщении не ограничен, что позволяет неаутентифицированному атакующему отправить специально сформированное PGP-сообщение с чрезмерно большим заявленным размером чанка, вызывая pre-auth (до какой-либо аутентификации/проверки подписи) истощение памяти/ресурсов при попытке его обработать.
Обоснование неприменимости: приложение не реализует функциональность приёма/расшифровки OpenPGP-сообщений через модуль bcpg — соответствующий парсер AEAD-пакетов не вызывается в системе.

CVE-2023-2976 (устаревшая, добавлена в NVD в 2023 г.)
Компонент: Google Guava, метод com.google.common.io.Files.createTempDir(). Тип: CWE-379 (Creation of Temporary File with Insecure Permissions). Механизм: метод создаёт временный каталог с правами доступа, зависящими от системного umask, что в многопользовательской POSIX-среде с общим /tmp может привести к тому, что другой локальный пользователь получит доступ на чтение/запись к временным файлам приложения — потенциальная утечка данных или атака через гонку (TOCTOU). Условие эксплуатации: вызов именно этого метода Guava + многопользовательская среда исполнения с общим временным каталогом.
Обоснование неприменимости: в кодовой базе метод Files.createTempDir() не вызывается (используется, например, java.nio.file.Files.createTempDirectory() с явно заданными безопасными правами доступа), либо приложение исполняется в изолированном/однопользовательском окружении без общего /tmp — условие эксплуатации отсутствует.

CVE-2026-54512 (CVSS 8.1, High)
Компонент: jackson-databind, метод DatabindContext._resolveAndValidateGeneric() в связке с BasicPolymorphicTypeValidator.validateSubType(). Тип: CWE-502 (Deserialization of Untrusted Data) / обход механизма защиты. Механизм: при включённом полиморфном тайпинге и наличии в строке идентификатора типа generic-параметров (символ <), метод валидирует по allow-list PolymorphicTypeValidator только «сырое» имя класса-контейнера (часть строки до <), но не проверяет вложенные типовые аргументы. Это позволяет атакующему указать разрешённый контейнер (например, java.util.ArrayList) с запрещённым классом в качестве generic-параметра (java.util.ArrayList<com.evil.Gadget>) — контейнер проходит проверку PTV, после чего вложенный класс загружается через Class.forName(), инстанцируется и заполняется данными из JSON, что при наличии подходящей gadget-цепочки в classpath приводит к RCE. Условие эксплуатации: приложение должно использовать полиморфную десериализацию Jackson (@JsonTypeInfo / default typing) с настроенным PolymorphicTypeValidator и обрабатывать JSON из недоверенного источника.
Обоснование неприменимости: полиморфная десериализация Jackson (@JsonTypeInfo/default typing) в проекте не включена — вся десериализация выполняется по фиксированным (не полиморфным) типам, поэтому код-путь _resolveAndValidateGeneric() с обходом PTV не вызывается независимо от версии библиотеки.
