"""Face Anonymizer - Video face anonymization tool."""

from face_anonymizer.detector import (
    MediaPipeDetector,
    YOLOFaceDetector,
    get_detector,
    FaceDetector,  # Backward compatibility
)
from face_anonymizer.anonymizer import blur, pixelate, black
from face_anonymizer.pipeline import VideoProcessor

__version__ = "1.0.0"
__all__ = [
    "MediaPipeDetector",
    "YOLOFaceDetector", 
    "get_detector",
    "FaceDetector",
    "blur",
    "pixelate", 
    "black",
    "VideoProcessor",
]