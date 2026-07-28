import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


class SyncLineageGateTest(unittest.TestCase):
    def test_inherited_daily_lineage_is_removed_before_atomic_publish(self):
        script = (REPO / "sync-posts.sh").read_text(encoding="utf-8")

        copy_at = script.index('cp -a "$LIVE_HTML/data" "$STAGING_DIR/data"')
        invalidate_at = script.index(
            'rm -f -- "$STAGING_DIR/data/${TODAY}.json"', copy_at
        )
        swap_at = script.index(
            'python3 "$REPO_DIR/atomic-swap.py" "$LIVE_HTML" "$STAGING_DIR"'
        )

        self.assertLess(copy_at, invalidate_at)
        self.assertLess(invalidate_at, swap_at)
        self.assertIn(
            '"$STAGING_DIR/data/${TODAY}-lineage.json"',
            script[invalidate_at:swap_at],
        )


if __name__ == "__main__":
    unittest.main()
