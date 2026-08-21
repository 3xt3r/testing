python - <<'PY'
from pathlib import Path
import subprocess

from cxxsca.checker_catalog import CheckerCatalog

CATALOG = Path("C:/Users/kolco/Desktop/checkers/catalog")

for p in CheckerCatalog().profiles:
    if not p.product or not p.vcs:
        print(f"[SKIP] {p.product or '?'}: no LINK_SOURCE")
        continue

    dst = CATALOG / p.product / "reference"
    dst.parent.mkdir(parents=True, exist_ok=True)

    if (dst / ".git").exists():
        print(f"[UPDATE] {p.product}")

        subprocess.run(
            ["git", "-C", str(dst), "pull", "--ff-only"],
            check=False,
        )
        subprocess.run(
            [
                "git", "-C", str(dst),
                "submodule", "update",
                "--init", "--recursive",
                "--depth", "1",
            ],
            check=False,
        )
    elif dst.exists():
        print(f"[SKIP] {p.product}: directory exists but is not git repo")
    else:
        print(f"[CLONE] {p.product}")

        subprocess.run(
            [
                "git", "clone",
                "--recursive",
                "--depth", "1",
                p.vcs,
                str(dst),
            ],
            check=False,
        )

print("\n[DONE]")
PY
