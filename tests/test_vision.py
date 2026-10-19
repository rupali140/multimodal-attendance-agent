
import unittest
from pathlib import Path

from modules.vision import detect_faces


class TestVision(unittest.TestCase):
    def test_missing_image_raises_error(self):
        missing_path = Path("tests/nonexistent_test_image.jpg")

        with self.assertRaises(FileNotFoundError):
            detect_faces(str(missing_path))


from modules.vision import CentroidTracker


class TestCentroidTracker(unittest.TestCase):
    def test_same_face_keeps_temporary_id(self):
        tracker = CentroidTracker(max_distance=100)

        first = tracker.update([(10, 10, 40, 40)])
        second = tracker.update([(12, 11, 40, 40)])

        self.assertEqual(list(first.keys()), list(second.keys()))

    def test_new_distant_face_gets_new_id(self):
        tracker = CentroidTracker(max_distance=30)

        first = tracker.update([(10, 10, 40, 40)])
        second = tracker.update([(300, 300, 40, 40)])

        self.assertNotEqual(list(first.keys()), list(second.keys()))

if __name__ == "__main__":
    unittest.main()
