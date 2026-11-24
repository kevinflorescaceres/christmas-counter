import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from app import app, compute_target

TZ = ZoneInfo("America/Santiago")


class ComputeTargetTest(unittest.TestCase):
    def test_before_christmas_targets_this_year(self):
        _, target = compute_target("America/Santiago", datetime(2026, 11, 24, 12, 0, tzinfo=TZ))
        self.assertEqual(target, datetime(2026, 12, 25, tzinfo=TZ))

    def test_christmas_day_still_targets_this_year(self):
        _, target = compute_target("America/Santiago", datetime(2026, 12, 25, 18, 0, tzinfo=TZ))
        self.assertEqual(target, datetime(2026, 12, 25, tzinfo=TZ))

    def test_day_after_christmas_targets_next_year(self):
        _, target = compute_target("America/Santiago", datetime(2026, 12, 26, 0, 0, tzinfo=TZ))
        self.assertEqual(target, datetime(2027, 12, 25, tzinfo=TZ))


class RoutesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_celebrates_on_christmas_day_without_js(self):
        now = datetime(2026, 12, 25, 18, 0, tzinfo=TZ)
        with patch("app.compute_target", return_value=(now, datetime(2026, 12, 25, tzinfo=TZ))):
            html = self.client.get("/").get_data(as_text=True)
        self.assertIn('id="celebrate">', html)
        self.assertIn('id="d">0<', html)

    def test_index_hides_celebration_before_christmas(self):
        now = datetime(2026, 11, 24, 12, 0, tzinfo=TZ)
        with patch("app.compute_target", return_value=(now, datetime(2026, 12, 25, tzinfo=TZ))):
            html = self.client.get("/").get_data(as_text=True)
        self.assertIn('id="celebrate" hidden>', html)


if __name__ == "__main__":
    unittest.main()
