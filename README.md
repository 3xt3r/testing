[confluence] attached: sources.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/origsbom.json)
2026-08-04 16:39:37 | INFO    | [confluence] attached: sources.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/origsbom.json)
[confluence] attached: docker_worker_1.13.2.cdx.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/docker_worker_1.13.2.cdx.json)
2026-08-04 16:39:39 | INFO    | [confluence] attached: docker_worker_1.13.2.cdx.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/docker_worker_1.13.2.cdx.json)
[confluence] attached: all_components.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/all_components.json)
2026-08-04 16:39:40 | INFO    | [confluence] attached: all_components.json (/home/csecuser/results/2026-08-04/Masking__develop/sbom/all_components.json)
2026-08-04 16:39:40 | INFO    | Updating page "test" with None
2026-08-04 16:39:41 | INFO    | Content of 260216953 differs
[confluence] OK: page 260216953 ('test') updated (source: 0 vulnerabilities; cplus: 0 vulnerabilities; 1 distrib(s))
2026-08-04 16:39:43 | INFO    | [confluence] OK: page 260216953 ('test') updated (source: 0 vulnerabilities; cplus: 0 vulnerabilities; 1 distrib(s))
  [merge-images] 1 image(s) -> 464 unique component(s), 0 unique vulnerabilit(y/ies)
2026-08-04 16:39:43 | INFO    | [images] [Masking__develop] merged 1 image SBOM(s) -> /home/csecuser/results/2026-08-04/Masking__develop/sbom/merged-images.json (464 components, 0 vulnerabilities)
2026-08-04 16:39:43 | INFO    | run log written: /home/csecuser/results/2026-08-04/run.log
2026-08-04 16:39:43 | INFO    | all 1 scan(s) completed successfully

metric	value							
components_total	16203							
vulnerable_components_c10f2	4							
findings_total_c10f2	7							
non_rpm_components	15739							
rpm_without_buildhost	0							
target_branch	c10f2							
mode	every RPM detected by Syft is treated as ALT RPM							
filter	c10f2 only							
								
package	version	source_rpm	buildhost	ecosystem	latest_c10f2	max_severity	findings_cve	vuln_ids
libidn	1.37-alt1	libidn-1.37-alt1.src.rpm		ALT RPM	1.44-alt1	LOW	1	CVE-2026-57053
libpolkit	0.120-alt3	polkit-0.120-alt3.src.rpm		ALT RPM	0.120-alt4	LOW	1	CVE-2026-4897
libssh2	1.11.0-alt2	libssh2-1.11.0-alt2.src.rpm		ALT RPM	1.11.1-alt3	CRITICAL	4	BDU:2026-08612, CVE-2026-55199, CVE-2026-55200, CVE-2026-7598
polkit	0.120-alt3	polkit-0.120-alt3.src.rpm		ALT RPM	0.120-alt4	LOW	1	CVE-2026-4897
