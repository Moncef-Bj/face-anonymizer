# Face Anonymizer


![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red)

Video face anonymization using MediaPipe and OpenCV.

## Features

- ✅ Real-time face detection with MediaPipe
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
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
uv pip install -e .
```

## Usage

### Webcam
```bash
python src/face_anonymizer/cli.py 0
```

### Video file
```bash
python src/face_anonymizer/cli.py video.mp4 blur 0.3
```

### Options
- Method: `blur`, `pixelate`, `black`
- Padding: `0.0` to `1.0` (margin around faces)
- Custom output: Add filename as last argument

## Examples
```bash
# Webcam with pixelate
python src/face_anonymizer/cli.py 0 pixelate 0.4

# Video with custom output
python src/face_anonymizer/cli.py input.mp4 blur 0.3 output.mp4
```

## Project Structure
```
face-anonymizer/
├── src/face_anonymizer/
│   ├── __init__.py      # Package initialization
│   ├── detector.py      # MediaPipe face detection
│   ├── anonymizer.py    # Blur, pixelate, black methods
│   ├── pipeline.py      # Video processing pipeline
│   └── cli.py           # Command-line interface
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── LICENSE             # MIT License
└── README.md           # Documentation

## Limitations

- Works best with close-up faces (selfies, video calls)
- May struggle with distant faces or crowded scenes
- MediaPipe optimized for frontal faces

## Future Improvements

- [ ] Add YOLOv8-Face detector for better distant face detection
- [ ] Add face tracking for consistent anonymization
- [ ] Support batch processing
- [ ] Add GUI interface

## License

MIT
```
