from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Proximity:
    face_detected: bool
    too_close: bool
    face_width_ratio: float | None


def estimate_proximity(frame, *, close_ratio: float = 0.35) -> Proximity:
    """Estimate face-to-camera proximity from one frame; this is not posture analysis."""
    import cv2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    if len(faces) == 0:
        return Proximity(False, False, None)
    frame_width = frame.shape[1]
    largest_width = max(width for _, _, width, _ in faces)
    ratio = largest_width / frame_width
    return Proximity(True, ratio >= close_ratio, round(float(ratio), 3))


def check_camera(camera_index: int = 0) -> Proximity:
    import cv2

    camera = cv2.VideoCapture(camera_index)
    try:
        if not camera.isOpened():
            raise RuntimeError("could not open camera; check that it is connected and permitted")
        ok, frame = camera.read()
        if not ok:
            raise RuntimeError("camera did not provide a frame")
        return estimate_proximity(frame)
    finally:
        camera.release()
