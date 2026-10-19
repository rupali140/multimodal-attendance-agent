
from pathlib import Path

import numpy as np
import soundfile as sf


def analyze_audio(audio_path: str, frame_seconds: float = 1.0) -> dict:
    """Measure audio RMS energy over fixed time intervals."""

    path = Path(audio_path)

    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if frame_seconds <= 0:
        raise ValueError("frame_seconds must be greater than 0")

    audio, sample_rate = sf.read(
        str(path),
        dtype="float32",
        always_2d=True,
    )

    if audio.shape[0] == 0:
        raise ValueError("Audio file is empty")

    # Convert multiple audio channels to mono.
    mono_audio = audio.mean(axis=1)

    samples_per_frame = max(1, int(sample_rate * frame_seconds))
    intervals = []

    for start in range(0, len(mono_audio), samples_per_frame):
        end = min(start + samples_per_frame, len(mono_audio))
        segment = mono_audio[start:end]

        rms = float(np.sqrt(np.mean(np.square(segment))))

        intervals.append({
            "start_seconds": round(start / sample_rate, 3),
            "end_seconds": round(end / sample_rate, 3),
            "rms": round(rms, 6),
        })

    return {
        "sample_rate": int(sample_rate),
        "duration_seconds": round(len(mono_audio) / sample_rate, 3),
        "intervals": intervals,
    }
