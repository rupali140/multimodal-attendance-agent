
import unittest

from modules.analytics import summarize_classroom


class TestClassroomAnalytics(unittest.TestCase):
    def setUp(self):
        self.analysis = {
            "vision": {"face_count": 2},
            "audio": {
                "intervals": [
                    {"rms": 0.0},
                    {"rms": 0.2},
                    {"rms": 0.2},
                ]
            },
        }

    def test_summary_values(self):
        result = summarize_classroom(self.analysis)

        self.assertEqual(result["face_count"], 2)
        self.assertEqual(result["audio_interval_count"], 3)
        self.assertAlmostEqual(result["average_rms"], 0.133333, places=5)
        self.assertEqual(result["sound_intensity"], "High")

    def test_empty_audio_intervals(self):
        self.analysis["audio"]["intervals"] = []

        result = summarize_classroom(self.analysis)

        self.assertEqual(result["audio_interval_count"], 0)
        self.assertEqual(result["average_rms"], 0.0)
        self.assertEqual(result["sound_intensity"], "Low")

    def test_engagement_limitation_is_included(self):
        result = summarize_classroom(self.analysis)

        self.assertIn("not a measure", result["interpretation"])


if __name__ == "__main__":
    unittest.main()
