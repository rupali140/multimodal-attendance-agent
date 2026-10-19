
import unittest

from modules.attendance import AttendanceTracker


class TestAttendanceTracker(unittest.TestCase):
    def test_present_after_minimum_observations(self):
        tracker = AttendanceTracker(min_observations=3)

        self.assertEqual(tracker.update([1])[1]["status"], "Pending")
        self.assertEqual(tracker.update([1])[1]["status"], "Pending")
        self.assertEqual(tracker.update([1])[1]["status"], "Present")

    def test_duplicate_ids_count_once_per_frame(self):
        tracker = AttendanceTracker(min_observations=2)

        tracker.update([1, 1, 1])
        result = tracker.update([1])

        self.assertEqual(result[1]["observations"], 2)
        self.assertEqual(result[1]["status"], "Present")

    def test_empty_frame_does_not_add_observations(self):
        tracker = AttendanceTracker(min_observations=2)

        tracker.update([1])
        result = tracker.update([])

        self.assertEqual(result[1]["observations"], 1)
        self.assertEqual(result[1]["status"], "Pending")

    def test_invalid_threshold_raises_error(self):
        with self.assertRaises(ValueError):
            AttendanceTracker(min_observations=0)


if __name__ == "__main__":
    unittest.main()
