import cv2
#from face_anonymizer.detector import get_detector
from face_anonymizer.anonymizer import blur, pixelate, black 
from datetime import datetime
from pathlib import Path


def generate_output_filename(input_path, method, padding, output_dir=None):
        """
        Génère un nom de fichier avec paramètres et timestamp.
        
        Args:
            input_path: Chemin du fichier source
            method: Méthode d'anonymisation
            padding: Valeur du padding
            output_dir: Dossier de sortie (optionnel)
            
        Returns:
            Chemin complet du fichier de sortie
        """
        input_path = Path(input_path)
        
        # Timestamp au format: 2024-12-16_14h30m15s
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        
        # Nom formaté: originalname_blur_p0.3_2024-12-16_14h30m15s.mp4
        output_name = f"{input_path.stem}_{method}_p{padding}_{timestamp}.mp4"
        
        # Dossier de sortie
        if output_dir:
            output_path = Path(output_dir) / output_name
        else:
            output_path = input_path.parent / output_name
        
        return str(output_path)

class VideoProcessor:
    """Traite une vidéo pour anonymiser les visages."""
    
    def __init__(self, method="blur", padding=0.3, detector_name="mediapipe", **kwargs):
        """
        Initialise le processeur vidéo.
        
        Args:
            method: Méthode d'anonymisation ("blur", "pixelate", "black")
            padding: Marge autour des visages (0.0 à 1.0)
            detector_name: "mediapipe" or "yolo"
            **kwargs: Arguments pour le détecteur (min_confidence, etc.)
        """
        self.method = method
        self.padding = padding
        from face_anonymizer.detector import get_detector
        self.detector = get_detector(detector_name, **kwargs)

    
    def _apply_padding(self, face, frame_width, frame_height):
        """
        Applique le padding à une détection.
        
        Args:
            face: Dictionnaire avec x, y, width, height
            frame_width: Largeur de la frame
            frame_height: Hauteur de la frame
            
        Returns:
            Dictionnaire avec coordonnées ajustées
        """
        x = face["x"]
        y = face["y"]
        width = face["width"]
        height = face["height"]
        
        # Calculer le padding
        pad_w = int(width * self.padding)
        pad_h = int(height * self.padding)
        
        # Agrandir
        x = x - pad_w
        y = y - pad_h
        width = width + (2 * pad_w)
        height = height + (2 * pad_h)
        
        # Limiter aux bords
        x = max(0, x)
        y = max(0, y)
        width = min(width, frame_width - x)
        height = min(height, frame_height - y)
    
        return {"x": x, "y": y, "width": width, "height": height}
    
    def process_frame(self, frame):
        """
        Traite une seule frame.
        
        Args:
            frame: Image BGR
            
        Returns:
            Frame avec visages anonymisés
        """
        h, w = frame.shape[:2]
        faces = self.detector.detect(frame)
        
        for face in faces:
            face = self._apply_padding(face, w, h)
            
            x = face["x"]
            y = face["y"]
            width = face["width"]
            height = face["height"]
            
            face_region = frame[y:y+height, x:x+width]
            
            if self.method == "blur":
                anonymized = blur(face_region)
            elif self.method == "pixelate":
                anonymized = pixelate(face_region)
            elif self.method == "black":
                anonymized = black(face_region)
            else:
                anonymized = face_region
            
            frame[y:y+height, x:x+width] = anonymized
        
        return frame
        
    
    
    def process_video(self, input_path, output_path=None):
        """
        Traite une vidéo complète.
        
        Args:
            input_path: Chemin vidéo source
            output_path: Chemin vidéo sortie (None = auto-généré)

        """
        if output_path is None:
            output_path = generate_output_filename(
            input_path, 
            self.method, 
            self.padding
            )
        # Ouvrir la vidéo source
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            raise ValueError(f"Impossible d'ouvrir la vidéo : {input_path}")
        
        # Récupérer les propriétés
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 Traitement: {input_path}")
        print(f"⚙️  FPS: {fps}, Taille: {frame_width}x{frame_height}")
        print(f"📊 Total frames: {frame_count}")
        print()
        
        # Créer le writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        # Traiter frame par frame
        processed_count = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Anonymiser la frame
                frame = self.process_frame(frame)
                
                # Écrire dans le fichier de sortie
                out.write(frame)
                
                # Afficher la frame (optionnel)
                cv2.imshow("Processing - Press 'q' to quit", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n⚠️  Arrêt demandé par l'utilisateur")
                    break
                
                processed_count += 1
                
                # Afficher progression tous les 30 frames
                if processed_count % 30 == 0:
                    progress = (processed_count / frame_count) * 100 if frame_count > 0 else 0
                    print(f"🔄 Progression: {processed_count}/{frame_count} frames ({progress:.1f}%)")
        
        finally:
            # Nettoyer (même en cas d'erreur)
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        
        print()
        print(f"✅ Terminé ! {processed_count} frames traitées")
        print(f"💾 Sauvegardé : {output_path}")
    
    def close(self):
        """Ferme les ressources."""
        self.detector.close()