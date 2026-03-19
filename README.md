# Alpa — Real-Time Face Swapper
> This simple project shows how simple it can be for someone to swap their face with AI.

## ⚠️ Disclaimer
This is a project I took on to further advance my Python programming. This tool is meant for research — any illegal activity falls on your responsibility.

*This tool does not store, transmit, or collect any data. All recordings are saved locally only.*

## Demo
- Live demo not provided for privacy reasons.
- See "How It Works" for a breakdown of the pipeline.

## Features
- **Real-Time Face Swapping:** Live webcam feed that swaps your face with any target image.
- **Session Recording:** Background recording with timestamped filenames saved locally.
- **Control Panel:** Tkinter GUI to select a target photo, toggle feed, and start recording.
- **Automatic Face Detection:** Built-in AI finds and tracks faces in the camera feed automatically.

## Requirements
- Python 3.10+
- NVIDIA GPU (CUDA)
- Webcam

## Installation
1. Clone the repo
```bash
git clone https://github.com/X3N0L4T/alpa.git
cd alpa
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Download the face swap model
   - Download `inswapper_128.onnx` from https://github.com/deepinsight/insightface/releases
   - Place it in the `models/` folder
4. Add a target face
   - Place any clear front-facing photo at `assets/target.jpg`
5. Run
```bash
python main.py
```

## Project Structure
```
alpa/
├── main.py          # GUI entry point
├── camera.py        # Camera detection and live frame capture
├── face_swap.py     # Face detection, model loading, and swap logic
├── logger.py        # Background MP4 recording with timestamped output
├── tracker.py       # Facial landmark tracking
├── requirements.txt # Python dependencies
├── models/          # Place inswapper_128.onnx here (not included)
└── assets/          # Place your target face image here as target.jpg
```

## How It Works
Every time your webcam captures a frame, your face gets quickly scanned to find where your eyes, nose, and mouth are. It then takes the target photo you provided and stretches it to fit the exact 3D shape of your face using InsightFace's InSwapper model.

## Cybersecurity Context
This project is a hands-on look at why we can't trust what we see on screen. Modern security systems like "liveness checks" — asking you to blink or smile to verify identity — can be bypassed using basic hardware and open source code. The goal is to raise awareness, specifically for more vulnerable groups like the elderly who may be targeted by deepfake scams.

## Project Status
> ⚠️ Work in progress

- **Quality:** Functional but can look glitchy depending on lighting and angles.
- **Performance:** Runs in real-time but has room for optimization on mid-range hardware.
- **Future Goals:** Better face blending and support for multiple target faces.