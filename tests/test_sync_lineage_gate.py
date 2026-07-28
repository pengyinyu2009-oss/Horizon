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

    def test_alert_runner_falls_back_when_horizon_venv_is_unavailable(self):
        script = (REPO / "sync-posts.sh").read_text(encoding="utf-8")
        alert_start = script.index("send_publish_alert()")
        alert_end = script.index("trap cleanup_staging", alert_start)
        alert_function = script[alert_start:alert_end]

        self.assertIn("command -v python3", alert_function)
        self.assertIn('"$python_bin" "$push_script"', alert_function)


if __name__ == "__main__":
    unittest.main()
