"""Face Anonymizer - Anonymisation de visages dans les vidéos."""

from face_anonymizer.detector import FaceDetector
from face_anonymizer import anonymizer

__version__ = "0.1.0"
__all__ = ["FaceDetector", "anonymizer"]