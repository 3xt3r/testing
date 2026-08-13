2026-08-13 12:44:20 | INFO    |     checkout test @ develop
2026-08-13 12:44:20 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** checkout -- .
2026-08-13 12:44:20 | ERROR   |     [FAIL] git checkout -- . (reset local changes): error: pathspec '.' did not match any file(s) known to git
2026-08-13 12:44:20 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** clean -fd
2026-08-13 12:44:20 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** checkout develop
2026-08-13 12:44:21 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** reset --hard origin/develop
2026-08-13 12:44:22 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** submodule update --init --recursive
2026-08-13 12:44:24 | INFO    |     cloning: https://gitlab.test.local/test/test
2026-08-13 12:44:24 | INFO    |     running: git -c credential.helper= clone --no-checkout https://gitlab.test.local/test/twst /home/csecuser/jobs/test/_repos/test
2026-08-13 12:44:24 | ERROR   |     [FAIL] git clone: Cloning into '/home/csecuser/jobs/test/_repos/test'...
fatal: could not read Username for 'https://gitlab.garda.local': terminal prompts disabled
2026-08-13 12:44:24 | INFO    |     clone without token failed — retrying with token
2026-08-13 12:44:24 | INFO    |     running: git -c credential.helper= -c http.extraHeader=Authorization: Basic *** clone --no-checkout https://gitlab.garda.local/garda-monitor/db_agent_total /home/test/jobs/NDR/_repos/test
