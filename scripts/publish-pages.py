"""Publish a validated Quartz build to gh-pages using the active gh account.

Build first: python scripts/kb.py build && npm --prefix site run build
This creates an ordinary fast-forward commit; it never rewrites remote history.
"""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Uptec-khj/gridex-power-policy-kb.git"


def run(args, cwd, capture=True):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=capture, text=True, encoding="utf-8").stdout.strip() if capture else subprocess.run(args, cwd=cwd, check=True)


if __name__ == "__main__":
    import sys
    run([sys.executable, "scripts/validate_kb.py", ".", "--site", "site/public"], ROOT, capture=False)
    # Local build check exercises the real Quartz search config and graph output.
    run(["node", "scripts/check-site.mjs"], ROOT, capture=False)
    public = ROOT / "site/public"
    if not (public / "index.html").is_file():
        raise SystemExit("Build site/public first")
    cache = (ROOT / ".cache").resolve()
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pages-publish-", dir=cache) as folder:
        staging = Path(folder).resolve()
        if not staging.is_relative_to(cache):
            raise SystemExit("Unexpected staging path")
        shutil.copytree(public, staging, dirs_exist_ok=True)
        (staging / ".nojekyll").write_text("", encoding="utf-8")
        git = ["git", "-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential"]
        run(git + ["init", "--quiet"], staging)
        run(git + ["add", "."], staging)
        tree = run(git + ["write-tree"], staging)
        parent_args = []
        existing = run(git + ["ls-remote", REPO, "refs/heads/gh-pages"], staging)
        if existing:
            run(git + ["fetch", "--quiet", "--depth=1", REPO, "gh-pages"], staging)
            parent_args = ["-p", run(git + ["rev-parse", "FETCH_HEAD"], staging)]
        source_sha = run(["git", "rev-parse", "HEAD"], ROOT)
        commit = run(git + ["commit-tree", tree, *parent_args, "-m", f"Publish GRIDEX from {source_sha}"], staging)
        run(git + ["push", REPO, f"{commit}:refs/heads/gh-pages"], staging, capture=False)
    print("Published build to gh-pages. GitHub Pages deployment status must be checked separately.")
