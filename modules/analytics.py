
def summarize_classroom(analysis_result: dict) -> dict:
    """Summarize face count and audio intensity without inferring engagement."""

    vision = analysis_result["vision"]
    audio = analysis_result["audio"]

    face_count = int(vision["face_count"])
    intervals = audio["intervals"]

    if face_count < 0:
        raise ValueError("face_count cannot be negative")

    rms_values = [float(item["rms"]) for item in intervals]

    if any(value < 0 for value in rms_values):
        raise ValueError("RMS values cannot be negative")

    average_rms = (
        sum(rms_values) / len(rms_values)
        if rms_values
        else 0.0
    )

    if average_rms < 0.01:
        intensity = "Low"
    elif average_rms < 0.1:
        intensity = "Moderate"
    else:
        intensity = "High"

    return {
        "face_count": face_count,
        "audio_interval_count": len(intervals),
        "average_rms": round(average_rms, 6),
        "sound_intensity": intensity,
        "interpretation": (
            "Sound intensity is not a measure of student engagement."
        ),
    }
