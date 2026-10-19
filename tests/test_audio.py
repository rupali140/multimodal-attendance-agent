
import tempfile
import unittest
from pathlib import Path

import numpy as np
import soundfile as sf

from modules.audio import analyze_audio


class TestAudioAnalysis(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.audio_path = Path(self.temp_dir.name) / "test.wav"

        sample_rate = 16000
        silence = np.zeros(sample_rate, dtype=np.float32)

        t = np.arange(sample_rate * 2) / sample_rate
        tone = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

        audio = np.concatenate([silence, tone])
        sf.write(str(self.audio_path), audio, sample_rate)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_duration_and_intervals(self):
        result = analyze_audio(str(self.audio_path))

        self.assertAlmostEqual(result["duration_seconds"], 3.0, places=2)
        self.assertEqual(len(result["intervals"]), 3)

    def test_silence_has_zero_rms(self):
        result = analyze_audio(str(self.audio_path))

        self.assertAlmostEqual(result["intervals"][0]["rms"], 0.0, places=5)

    def test_tone_has_positive_rms(self):
        result = analyze_audio(str(self.audio_path))

        self.assertGreater(result["intervals"][1]["rms"], 0.1)

    def test_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            analyze_audio("missing_audio_file.wav")

    def test_invalid_frame_duration_raises_error(self):
        with self.assertRaises(ValueError):
            analyze_audio(str(self.audio_path), frame_seconds=0)


if __name__ == "__main__":
    unittest.main()
