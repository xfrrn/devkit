import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "packages" / "project-docs" / "scripts" / "init_project_docs.py"


class InitProjectDocsTest(unittest.TestCase):
    def run_script(self, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(target), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_default_is_core_and_all_is_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.assertEqual(self.run_script(target).returncode, 0)
            self.assertEqual(
                {path.name for path in (target / "docs").iterdir()},
                {"00-project-brief.md", "01-requirements.md", "02-system-design.md"},
            )
            self.assertEqual(self.run_script(target, "--all").returncode, 0)
            self.assertTrue((target / "docs" / "09-progress-log.md").is_file())

    def test_docs_dir_cannot_escape_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            result = self.run_script(target, "--docs-dir", "../outside")
            self.assertEqual(result.returncode, 2)
            self.assertFalse((Path(directory) / "outside").exists())


if __name__ == "__main__":
    unittest.main()
