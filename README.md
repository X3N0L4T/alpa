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
- **Control Panel:** PyQt6 GUI to select a target photo, toggle feed, and start recording.
- **Automatic Face Detection:** Built-in AI finds and tracks faces in the camera feed automatically.
- **Facial Landmark Overlay:** MediaPipe FaceMesh draws a real-time mesh over detected faces showing what the AI is tracking.

## Requirements
- Python 3.11
- NVIDIA GPU (CUDA 11.x or 12.x recommended — see Known Issues)
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
3. Create required folders
```bash
mkdir models
mkdir assets
```
4. Download the face swap model
   - Download `inswapper_128.onnx` from https://github.com/deepinsight/insightface/releases
   - Place it in the `models/` folder
5. Add a target face
   - Place any clear front-facing photo at `assets/target.jpg`
6. Run
```bash
python main.py
```

## Project Structure
```
alpa/
├── main.py          # GUI entry point, wires all modules together
├── camera.py        # Camera detection and live frame capture
├── face_swap.py     # Face detection, model loading, and swap logic
├── logger.py        # Background MP4 recording with timestamped output
├── tracker.py       # Facial landmark mesh overlay via MediaPipe
├── requirements.txt # Python dependencies
├── models/          # Place inswapper_128.onnx here (not included)
└── assets/          # Place your target face image here as target.jpg
```

## How It Works
Every time your webcam captures a frame, your face gets quickly scanned to find where your eyes, nose, and mouth are. It then takes the target photo you provided and stretches it to fit the exact 3D shape of your face using InsightFace's InSwapper model. Simultaneously, MediaPipe draws a 468-point landmark mesh over your face showing exactly what the AI is seeing and tracking in real time.

## Cybersecurity Context
This project is a hands-on look at why we can't trust what we see on screen. Modern security systems like "liveness checks" — asking you to blink or smile to verify identity — can be bypassed using basic hardware and open source code. The goal is to raise awareness, specifically for more vulnerable groups like the elderly who may be targeted by deepfake scams.

## Known Issues & Project Status
> ⚠️ Work in progress

- **Performance:** The live feed and face swap currently run on CPU rather than GPU. This is due to a compatibility issue between CUDA 13.1 (installed on the development machine) and `onnxruntime-gpu`, which only supports up to CUDA 12.x at this time. As a result, the live feed may feel slow or delayed — this is a known limitation being actively worked on. Users with CUDA 11.x or 12.x should see slightly better performance.
- **Tracker Flicker:** The facial landmark overlay runs every 3rd frame to reduce CPU load. On slower machines this may still cause visible lag.
- **Quality:** The face swap is functional but can look glitchy or unnatural depending on lighting and camera angle.
- **Future Goals:** GPU acceleration once onnxruntime adds CUDA 13 support, better face blending, camera selector dropdown, and a swap toggle control.