import cv2


class BaseDetector:
    """Base class for face detectors."""
    
    def detect(self, frame):
        raise NotImplementedError
    
    def close(self):
        pass

# ============================================
# MEDIAPIPE DETECTOR
# ============================================
class MediaPipeDetector(BaseDetector):
    """Face detector using MediaPipe. Best for selfies/webcam."""
    
    def __init__(self, min_confidence=0.3, model_selection=1):
        import mediapipe as mp
        
        mp_face_detection = mp.solutions.face_detection
        self.detector = mp_face_detection.FaceDetection(
            min_detection_confidence=min_confidence,
            model_selection=model_selection
        )
    
    def detect(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_frame)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                faces.append({
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                })
        return faces
    
    def close(self):
        self.detector.close()

# ============================================
# YOLO FACE DETECTOR
# ============================================
class YOLOFaceDetector(BaseDetector):
    """Face detector using YOLOv8-Face. Best for distant faces."""
    
    def __init__(self, min_confidence=0.3, model_path=None):
        from ultralytics import YOLO
        
        # Use yolov8n-face model
        if model_path is None:
            
            model_path = "models/yolov8n-face.pt"
        
        self.model = YOLO(model_path)
        self.min_confidence = min_confidence
        
        print(f"✅ YOLO model loaded: {model_path}")
    
    def detect(self, frame):
        # Run inference (class 0 = face for face models)
        results = self.model(frame, verbose=False, conf=self.min_confidence)
        
        faces = []
        for result in results:
            boxes = result.boxes
            
            if boxes is None:
                continue
                
            for box in boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                x = int(x1)
                y = int(y1)
                width = int(x2 - x1)
                height = int(y2 - y1)
                
                # Ensure valid dimensions
                if width > 0 and height > 0:
                    faces.append({
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height
                    })
        
        return faces
    
    def close(self):
        pass  # YOLO doesn't need explicit cleanup

# ============================================
# FACTORY FUNCTION
# ============================================
def get_detector(name="mediapipe", **kwargs):
    """
    Factory function to get a detector by name.
    
    Args:
        name: "mediapipe" or "yolo"
        **kwargs: Arguments for the detector
        
    Returns:
        Detector instance
    """
    detectors = {
        "mediapipe": MediaPipeDetector,
        "yolo": YOLOFaceDetector,
    }
    
    if name not in detectors:
        raise ValueError(f"Unknown detector: {name}. Choose from: {list(detectors.keys())}")
    
    print(f"🎯 Using detector: {name}")
    return detectors[name](**kwargs)


# ============================================
# BACKWARD COMPATIBILITY
# ============================================
FaceDetector = MediaPipeDetector