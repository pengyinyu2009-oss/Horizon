import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


class AtomicSwapTest(unittest.TestCase):
    def test_exchanges_two_nonempty_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left"
            right = root / "right"
            left.mkdir()
            right.mkdir()
            (left / "old.txt").write_text("old", encoding="utf-8")
            (right / "new.txt").write_text("new", encoding="utf-8")

            subprocess.run(
                [sys.executable, str(REPO / "atomic-swap.py"), str(left), str(right)],
                check=True,
            )

            self.assertEqual((left / "new.txt").read_text(encoding="utf-8"), "new")
            self.assertEqual((right / "old.txt").read_text(encoding="utf-8"), "old")


if __name__ == "__main__":
    unittest.main()
