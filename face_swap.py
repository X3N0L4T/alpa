import os
os.environ["CUDA_PATH"] = ""
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import cv2
import insightface
from insightface.app import FaceAnalysis
import numpy as np
import os

def initialize_model():
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))

    swapper = insightface.model_zoo.get_model(
        "models/inswapper_128.onnx",
        download=False
    )

    print("[~ ALPA ~] Models loaded successfully")
    return app, swapper


def load_target_face(image_path, app):
    img = cv2.imread(image_path)

    if img is None:
        print(f"[~ ERROR ~] Could not load image: {image_path}")
        return None

    faces = app.get(img)

    if not faces:
        print("[~ ERROR ~] No face detected in target image")
        return None

    print(f"[~ INFO ~] Target face loaded from {image_path}")
    return faces[0]  # Use the first detected face


def swap_current_face(frame, target_face, app, swapper):
    faces = app.get(frame)

    if not faces:
        return frame

    for face in faces:
        frame = swapper.get(frame, face, target_face, paste_back=True)

    return frame

def main():
    app, swapper = initialize_model()

    target_path = "assets/target.jpg"
    target_face = load_target_face(target_path, app)

    if target_face is None:
        print(f"[~ ERROR ~] Target face could not be loaded from {target_path}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"[~ ERROR ~] Could not access camera")
        return

    print(f"[~ INFO ~] Target face loaded, starting swap session...")
    print(f"[~ INFO ~] Press 'q' to exit")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            swap_frame = swap_current_face(frame, target_face, app, swapper)

            cv2.imshow("frame", swap_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"[~ INFO ~] Session ended")

if __name__ == "__main__":
    main()
