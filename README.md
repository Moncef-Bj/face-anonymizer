# Face Anonymizer


![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Face-red)

Video face anonymization using MediaPipe and YOLOv8-Face.

## Features

- ✅ Real-time face detection with MediaPipe
- ✅ **2 detectors**: MediaPipe (selfies) & YOLOv8-Face (distant faces)
- ✅ 3 anonymization methods: Blur, Pixelate, Black
- ✅ Works with webcam or video files
- ✅ Automatic output naming with timestamps
- ✅ Configurable padding and confidence    

## Installation
```bash
# Clone the repo
git clone https://github.com/Moncef-Bj/face-anonymizer.git
cd face-anonymizer

# Create virtual environment
uv venv --python 3.11
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
uv pip install -e .
```

## Usage


```bash
python src/face_anonymizer/cli.py INPUT [method] [padding] [detector]
```

### Arguments

| Argument | Options | Default | Description |
|----------|---------|---------|-------------|
| INPUT | file.mp4 or 0 | required | Video file or webcam |
| method | blur, pixelate, black | blur | Anonymization method |
| padding | 0.0 - 1.0 | 0.3 | Margin around faces |
| detector | mediapipe, yolo | mediapipe | Detection model |

### Detectors

| Detector | Best for | Speed |
|----------|----------|-------|
| `mediapipe` | Selfies, webcam, close faces | ⚡ Fast |
| `yolo` | Videos, distant faces, crowds | 🎯 Accurate |

## Examples
```bash
# Webcam with MediaPipe (default, good for selfies)
python src/face_anonymizer/cli.py 0

# Webcam with YOLOv8-Face (better for distant faces)
python src/face_anonymizer/cli.py 0 blur 0.3 yolo

# Video file with pixelate effect
python src/face_anonymizer/cli.py video.mp4 pixelate 0.4 yolo

# Video with black rectangles
python src/face_anonymizer/cli.py input.mp4 black 0.3 mediapipe
```

## Project Structure
```
face-anonymizer/
├── src/face_anonymizer/
│   ├── __init__.py      # Package initialization
│   ├── detector.py      # MediaPipe & YOLOv8 detectors
│   ├── anonymizer.py    # Blur, pixelate, black methods
│   ├── pipeline.py      # Video processing pipeline
│   └── cli.py           # Command-line interface
├── models/
│   └── yolov8n-face.pt  # YOLOv8-Face model
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
└── README.md
```

## Limitations

- MediaPipe works best with close-up frontal faces
- YOLOv8-Face better for varied conditions but slower
- Very small faces may still be missed

## Future Improvements

- [ ] Add face tracking for consistent IDs across frames
- [ ] Add GUI interface (Gradio/Streamlit)
- [ ] Support batch processing
- [ ] Add Docker support

## License

MIT
```
