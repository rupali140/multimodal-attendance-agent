
from pathlib import Path

import cv2


def detect_faces(image_path: str) -> dict:
    """Detect faces in an image using OpenCV's Haar Cascade."""
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Could not read image: {path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cascade_path = (
        Path(cv2.data.haarcascades)
        / "haarcascade_frontalface_default.xml"
    )
    detector = cv2.CascadeClassifier(str(cascade_path))

    if detector.empty():
        raise RuntimeError("Could not load the face-detection model.")

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    return {
        "image": image,
        "face_count": len(faces),
        "boxes": [tuple(map(int, face)) for face in faces],
    }


def annotate_faces(image, boxes):
    """Draw rectangles around detected faces."""
    result = image.copy()

    for x, y, width, height in boxes:
        cv2.rectangle(
            result,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2,
        )

    return result

def analyze_video_frames(video_path: str, every_n_frames: int = 15) -> dict:
    """Sample video frames and count detected faces in each sampled frame."""
    from pathlib import Path

    path = Path(video_path)

    if not path.is_file():
        raise FileNotFoundError(f"Video not found: {path}")

    if every_n_frames < 1:
        raise ValueError("every_n_frames must be at least 1")

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        raise ValueError(f"Could not open video: {path}")

    frame_index = 0
    sampled_frames = 0
    total_faces = 0
    observations = []

    try:
        while True:
            success, frame = capture.read()

            if not success:
                break

            if frame_index % every_n_frames == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                cascade_path = (
                    Path(cv2.data.haarcascades)
                    / "haarcascade_frontalface_default.xml"
                )
                detector = cv2.CascadeClassifier(str(cascade_path))

                if detector.empty():
                    raise RuntimeError("Could not load face-detection model.")

                faces = detector.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                )

                count = len(faces)
                sampled_frames += 1
                total_faces += count

                observations.append({
                    "frame": frame_index,
                    "face_count": count,
                })

            frame_index += 1
    finally:
        capture.release()

    return {
        "frames_read": frame_index,
        "sampled_frames": sampled_frames,
        "total_face_detections": total_faces,
        "observations": observations,
    }

import math


class CentroidTracker:
    """Assign temporary IDs to detections based on centroid distance."""

    def __init__(self, max_distance: float = 100.0, max_missing: int = 5):
        self.max_distance = max_distance
        self.max_missing = max_missing
        self.next_id = 1
        self.tracks = {}

    @staticmethod
    def _centroid(box):
        x, y, width, height = box
        return (x + width / 2, y + height / 2)

    def update(self, boxes):
        """Update tracks using bounding boxes from the current frame."""
        detections = [tuple(map(int, box)) for box in boxes]

        # Age existing tracks; unmatched tracks may survive briefly.
        for track in self.tracks.values():
            track["missing"] += 1

        available_tracks = set(self.tracks.keys())
        assignments = {}

        # Match each detection to its nearest eligible existing track.
        for box in detections:
            center = self._centroid(box)
            candidates = []

            for track_id in available_tracks:
                old_center = self.tracks[track_id]["centroid"]
                distance = math.dist(center, old_center)

                if distance <= self.max_distance:
                    candidates.append((distance, track_id))

            if candidates:
                _, track_id = min(candidates)
                self.tracks[track_id]["centroid"] = center
                self.tracks[track_id]["box"] = box
                self.tracks[track_id]["missing"] = 0
                available_tracks.remove(track_id)
            else:
                track_id = self.next_id
                self.next_id += 1
                self.tracks[track_id] = {
                    "centroid": center,
                    "box": box,
                    "missing": 0,
                }

            assignments[track_id] = box

        # Remove tracks absent for too long.
        expired = [
            track_id
            for track_id, track in self.tracks.items()
            if track["missing"] > self.max_missing
        ]

        for track_id in expired:
            del self.tracks[track_id]

        return assignments
