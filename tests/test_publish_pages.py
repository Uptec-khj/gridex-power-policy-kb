import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("publish_pages", Path(__file__).resolve().parents[1] / "scripts/publish-pages.py")
publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish)


class PublicationGateTests(unittest.TestCase):
    def test_clean_remote_main_allowed(self):
        with patch.object(publish, "run", side_effect=["", "", "", "abc", "abc\trefs/heads/main"]):
            self.assertEqual(publish.require_merged_clean(), "abc")

    def test_uncommitted_or_staged_changes_blocked(self):
        for responses in (["content/test.md"], ["", "content/staged.md"]):
            with self.subTest(responses=responses), patch.object(publish, "run", side_effect=responses):
                with self.assertRaisesRegex(RuntimeError, "clean checkout"):
                    publish.require_merged_clean()

    def test_untracked_changes_blocked(self):
        with patch.object(publish, "run", side_effect=["", "", "content/new.md"]):
            with self.assertRaisesRegex(RuntimeError, "clean checkout"):
                publish.require_merged_clean()

    def test_unmerged_or_outdated_commit_blocked(self):
        with patch.object(publish, "run", side_effect=["", "", "", "abc", "def\trefs/heads/main"]):
            with self.assertRaisesRegex(RuntimeError, "remote main"):
                publish.require_merged_clean()

    def test_missing_main_blocked(self):
        with patch.object(publish, "run", side_effect=["", "", "", "abc", ""]):
            with self.assertRaisesRegex(RuntimeError, "remote main"):
                publish.require_merged_clean()

    def test_remote_error_propagates(self):
        with patch.object(publish, "run", side_effect=subprocess.CalledProcessError(1, ["git"])):
            with self.assertRaises(subprocess.CalledProcessError):
                publish.require_merged_clean()

    def test_existing_workflow_preserved_without_stale_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git = ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "core.autocrlf=false"]
            publish.run(git + ["init", "--quiet"], root)
            workflow = root / ".github/workflows/publish-current.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_bytes(b"name: existing\non: push\n")
            (root / "old.json").write_text("old full text", encoding="utf-8")
            publish.run(git + ["add", "."], root)
            old_tree = publish.run(git + ["write-tree"], root)
            publish.run(git + ["read-tree", "--empty"], root)
            (root / "index.html").write_text("new public summary", encoding="utf-8")
            publish.run(git + ["add", "index.html"], root)
            publish.preserve_workflows(git, root, old_tree)
            new_tree = publish.run(git + ["write-tree"], root)
            paths = publish.run(git + ["ls-tree", "-r", "--name-only", new_tree], root).splitlines()
            self.assertEqual(paths, [".github/workflows/publish-current.yml", "index.html"])
            for tree in (old_tree, new_tree):
                self.assertEqual(publish.run(git + ["show", f"{tree}:.github/workflows/publish-current.yml"], root), "name: existing\non: push")

    def test_symlink_workflow_blocked(self):
        with patch.object(publish, "run", return_value="120000 blob abc\t.github/workflows/symlink.yml\0"):
            with self.assertRaisesRegex(RuntimeError, "Unexpected"):
                publish.preserve_workflows(["git"], Path("."), "parent")


if __name__ == "__main__":
    unittest.main()
