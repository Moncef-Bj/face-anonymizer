# Face Anonymizer

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
git clone https://github.com/YOUR_USERNAME/face-anonymizer.git
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
