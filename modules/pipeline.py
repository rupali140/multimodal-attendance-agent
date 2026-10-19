
from pathlib import Path

from modules.audio import analyze_audio
from modules.vision import detect_faces


def analyze_classroom(
    image_path: str,
    audio_path: str,
    frame_seconds: float = 1.0,
) -> dict:
    """Combine image-based face counts and audio energy analysis."""

    image_file = Path(image_path)
    audio_file = Path(audio_path)

    if not image_file.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not audio_file.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    vision_result = detect_faces(str(image_file))
    audio_result = analyze_audio(
        str(audio_file),
        frame_seconds=frame_seconds,
    )

    return {
        "vision": {
            "face_count": vision_result["face_count"],
        },
        "audio": {
            "sample_rate": audio_result["sample_rate"],
            "duration_seconds": audio_result["duration_seconds"],
            "intervals": audio_result["intervals"],
        },
        "limitations": [
            "Face count does not establish identity or attendance.",
            "Audio energy does not prove speech or engagement.",
            "Image and audio results are not yet synchronized.",
        ],
    }
