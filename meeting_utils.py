"""Meeting link utilities for video consultations."""
import uuid


def create_meeting_link(appointment_id=None):
    """Generate a unique meeting link for video consultations.
    Returns dict with room_id and jitsi_link for video_db compatibility.
    """
    room_id = uuid.uuid4().hex[:10]
    jitsi_link = f"https://meet.jit.si/expertease-{room_id}"
    return {"room_id": room_id, "jitsi_link": jitsi_link}
