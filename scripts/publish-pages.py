"""Publish a validated Quartz build to gh-pages using the active gh account.

Only clean, merged source is published. Rebuild before publishing; preserve
existing deployment workflows byte-for-byte and never rewrite remote history.
"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Uptec-khj/gridex-power-policy-kb.git"


def run(args, cwd, capture=True):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=capture, text=True, encoding="utf-8").stdout.strip() if capture else subprocess.run(args, cwd=cwd, check=True)


def require_merged_clean(root=ROOT, repo=REPO):
    if (run(["git", "diff", "--name-only"], root)
            or run(["git", "diff", "--cached", "--name-only"], root)
            or run(["git", "ls-files", "--others", "--exclude-standard"], root)):
        raise RuntimeError("Publish requires a clean checkout; review and commit changes first")
    source_sha = run(["git", "rev-parse", "HEAD"], root)
    remote = run(["git", "ls-remote", repo, "refs/heads/main"], root).split()
    if not remote or remote[0] != source_sha:
        raise RuntimeError("Publish only the current remote main after PR review/merge")
    return source_sha


def preserve_workflows(git, staging, parent):
    # Retain only existing workflow blobs, not stale site pages or full text.
    entries = run(git + ["ls-tree", "-r", "-z", parent, "--", ".github/workflows"], staging)
    for entry in filter(None, entries.split("\0")):
        metadata, path = entry.split("\t", 1)
        mode, kind, oid = metadata.split()
        if kind != "blob" or mode not in {"100644", "100755"} or not path.startswith(".github/workflows/"):
            raise RuntimeError("Unexpected deployment workflow entry")
        run(git + ["update-index", "--add", "--cacheinfo", f"{mode},{oid},{path}"], staging)


if __name__ == "__main__":
    import sys
    source_sha = require_merged_clean()
    npm = "npm.cmd" if os.name == "nt" else "npm"
    run([npm, "--prefix", "site", "run", "build"], ROOT, capture=False)
    require_merged_clean()  # deterministic build; main must not have advanced
    run([sys.executable, "scripts/validate_kb.py", ".", "--site", "site/public"], ROOT, capture=False)
    # Local build check exercises the real Quartz search config and graph output.
    run(["node", "scripts/check-site.mjs"], ROOT, capture=False)
    public = ROOT / "site/public"
    if not (public / "index.html").is_file():
        raise SystemExit("Build site/public first")
    if (public / ".github").exists():
        raise SystemExit("Build output must not supply GitHub workflow configuration")
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
        parent_args = []
        existing = run(git + ["ls-remote", REPO, "refs/heads/gh-pages"], staging)
        if existing:
            run(git + ["fetch", "--quiet", "--depth=1", REPO, "gh-pages"], staging)
            parent = run(git + ["rev-parse", "FETCH_HEAD"], staging)
            parent_args = ["-p", parent]
            preserve_workflows(git, staging, parent)
        tree = run(git + ["write-tree"], staging)
        if require_merged_clean() != source_sha:
            raise SystemExit("Source changed during publication; rebuild and retry")
        commit = run(git + ["commit-tree", tree, *parent_args, "-m", f"Publish GRIDEX from {source_sha}"], staging)
        run(git + ["push", REPO, f"{commit}:refs/heads/gh-pages"], staging, capture=False)
    print("Published build to gh-pages. GitHub Pages deployment status must be checked separately.")
