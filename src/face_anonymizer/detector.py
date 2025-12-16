import cv2
import mediapipe as mp 


class FaceDetector:
    def __init__(self, min_confidence=0.3, model_selection=1):
        """
        Initialise le détecteur.
        
        Args:
            min_confidence: Seuil de confiance (0.0 à 1.0)
            model_selection: 0 = proche, 1 = loin
        """
        mp_face_detection = mp.solutions.face_detection
        self.detector = mp_face_detection.FaceDetection(
            min_detection_confidence=min_confidence,
            model_selection=model_selection
            )

        
    
    def detect(self, frame):
        """
        Détecte les visages dans une frame.
        
        Args:
            frame: Image BGR (numpy array)
            
        Returns:
            Liste de dictionnaires avec x, y, width, height
        """
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_frame)

        faces = []  # Liste pour stocker les visages détectés
        if results.detections:
            for detection in results.detections: 
                bbox = detection.location_data.relative_bounding_box

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width *w)
                height =  int(bbox.height* h)

                faces.append({
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                })
        return faces
    
    def close(self):
        """
        Libere les ressources 
        """
        self.detector.close()