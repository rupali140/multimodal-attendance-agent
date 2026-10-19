
from collections import defaultdict


class AttendanceTracker:
    """Track repeated observations of temporary participant IDs."""

    def __init__(self, min_observations: int = 3):
        if min_observations < 1:
            raise ValueError("min_observations must be at least 1")

        self.min_observations = min_observations
        self.observations = defaultdict(int)

    def update(self, participant_ids):
        """Record IDs observed in the current sampled frame."""
        for participant_id in set(participant_ids):
            self.observations[participant_id] += 1

        return self.get_attendance()

    def get_attendance(self):
        """Return observation counts and provisional attendance status."""
        return {
            participant_id: {
                "observations": count,
                "status": (
                    "Present"
                    if count >= self.min_observations
                    else "Pending"
                ),
            }
            for participant_id, count in self.observations.items()
        }
