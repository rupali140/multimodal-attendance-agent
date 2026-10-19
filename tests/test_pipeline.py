
import unittest
from pathlib import Path

from modules.pipeline import analyze_classroom


class TestClassroomPipeline(unittest.TestCase):
    def setUp(self):
        self.image_path = Path("data/classroom_test.jpg")
        self.audio_path = Path("data/audio_test.wav")

    def test_missing_image_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            analyze_classroom(
                "data/missing_image.jpg",
                str(self.audio_path),
            )

    def test_missing_audio_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            analyze_classroom(
                str(self.image_path),
                "data/missing_audio.wav",
            )

    def test_combined_analysis(self):
        if not self.image_path.is_file() or not self.audio_path.is_file():
            self.skipTest("Test image or audio file is missing")

        result = analyze_classroom(
            str(self.image_path),
            str(self.audio_path),
        )

        self.assertIn("vision", result)
        self.assertIn("audio", result)
        self.assertIn("face_count", result["vision"])
        self.assertIn("intervals", result["audio"])
        self.assertIn("limitations", result)


if __name__ == "__main__":
    unittest.main()
