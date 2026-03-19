=> Alpa — Real-Time Face Swapper
    > This simple project shows how simple it can be for someone to swap their face with AI.

=> Disclaimer
    ~ This is a project I took on to further advance my Python programming. This project/tool is
    meant for research, if any illegal activity is done with this, it falls on your responsibility.

    *This tool does not store, transmit, or collect any data. All recordings are saved locally only.*

=> Demo
    ~ Live demo not provided for privacy reasons.
    ~ See "How it works" for a breakdown of the pipeline.

=> Features

    • Real-Time Face Swapping: Live webcam feed that swaps your face with any target image.

    • Session Recording: Capture your results with background recording and organized, timestamp
      filenames saved locally.

    • Control Panel: A simple GUI built with Tkinter lets you select a target photo, toggle camera feed,
      and start recording.

    • Automatic Face Detection: Uses built in AI to find and track faces in the camera feed automatically.

=> Requirements
    ~ Python 3.10+
    ~ NVIDIA GPU (CUDA)
    ~ Webcam

=> Installation
    1. Clone the repo
        ~ #update after you make the repo
        ~ cd alpa

    2. Install dependencies
        ~ pip install -r requirements.txt

    3. Download the face swap model
        ~ Download inswapper_128.onnx from: https://github.com/deepinsight/insightface/releases
        ~ Place it in models/ folder

    4. Add target face
        ~ Place any clear front-facing photo in assets/target.jpg

    5. Run
        ~ python main.py

=> Project Structure
    alpa/
    ├── main.py          # GUI entry point, wires all modules together
    ├── camera.py        # Camera detection and live frame capture
    ├── face_swap.py     # Face detection, model loading, and swap logic
    ├── logger.py        # Background MP4 recording with timestamped output
    ├── requirements.txt # Python dependencies
    ├── models/          # Place inswapper_128.onnx here (not included)
    └── assets/          # Place your target face image here as target.jpg

=> How It Works
    ~ Every time your webcam captures a frame, your face gets quickly "scanned" to find where your
    eyes, nose, and mouth are. It then takes the target photo you provided and stretches it to fit
    the exact 3D shape.

=> Cybersecurity Context
    ~ This project is a hands on look at why we can't trust what we see on screen. Modern security systems
      like "liveness checks" (asking you to blink or smile) to verify identity, but this tool demonstrates
      how these can be bypassed using basic hardware and open source code. By showing that real-time video can be
      faked on a standard home computer, the goal here is to raise awareness-specifically the more vulnerable groups,
      like the elderly, who may be targeted by sophisticated deepfake scams.

=> Project Status
    *Please Note: This project is far from done, it's still a work in progress.

    • Quality: The face swap is functional but can look "glitchy" or unnatural depending on
      lighting and angles.

    • Performance: While it runs in real-time, there is still significant room for optimization
      to make it smoother and mid-range hardware.

    • Future Goals: I'm looking at adding better face blending and support mixing different targets.