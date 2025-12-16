import cv2

def blur(face_region, strength=99):
    """
    Applique un flou gaussien.
    
    Args:
        face_region: Zone du visage (numpy array)
        strength: Intensité du flou (impair)
        
    Returns:
        Image floutée
    """
    anonymized = cv2.GaussianBlur(face_region, (strength, strength), 0)
    
    return anonymized


def pixelate(face_region, pixel_size=10):
    """
    Applique une pixelisation.
    
    Args:
        face_region: Zone du visage
        pixel_size: Taille des blocs
        
    Returns:
        Image pixelisée
    """
    h, w = face_region.shape[:2]
    small = cv2.resize(face_region, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
    anonymized = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    
    return anonymized


def black(face_region):
    """
    Remplace par du noir.    
    Args:
        face_region: Zone du visage
        
    Returns:
        Image noire
    """
    anonymized = face_region.copy()
    anonymized[:] = 0
    return anonymized