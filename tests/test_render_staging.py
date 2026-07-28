import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


class RenderStagingTest(unittest.TestCase):
    def test_renders_to_staging_without_touching_live_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "reports"
            staging = root / "staging"
            live = root / "live"
            src.mkdir()
            live.mkdir()
            (live / "sentinel.html").write_text("old-live", encoding="utf-8")
            for section in ("horizon", "ee", "embedded", "oshw"):
                (src / f"2026-07-28-{section}-zh.md").write_text(
                    f"# 2026-07-28 {section}\n\ncontent\n",
                    encoding="utf-8",
                )

            subprocess.run(
                [
                    sys.executable,
                    str(REPO / "render-html.py"),
                    "--src",
                    str(src),
                    "--dst",
                    str(staging),
                ],
                check=True,
                env=os.environ.copy(),
            )

            self.assertIn("2026-07-28", (staging / "2026-07-28.html").read_text())
            self.assertEqual((live / "sentinel.html").read_text(), "old-live")


if __name__ == "__main__":
    unittest.main()
