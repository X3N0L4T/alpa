import cv2
import os
from datetime import datetime

def create_recording_dir(folder="recordings"):
    if not os.path.exists(folder):
        print(f"[~ INFO ~] Creating folder {folder}")
        os.makedirs(folder)
    return folder

def start_recording(fps=20.0, resolution=(640, 480)):
    folder = create_recording_dir()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"alpa_{timestamp}.mp4"
    filepath = os.path.join(folder, filename)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(filepath, fourcc, fps, resolution)

    print(f"[~ INFO ~] Starting recording: {filepath}")
    return writer, filepath


def write_frames(writer, frames):
    writer.write(frames)

def stop_recording(writer):
    writer.release()
    print("[~ INFO ~] Stopped recording, and saved")

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[~ ERROR ~] Unable to open camera")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer, filepath = start_recording(fps=20.0, resolution=(frame_width, frame_height))

    print(f"[~ INFO ~] Recording to: {filepath}")
    print(f"[~ INFO ~] Press 'q' to stop recording and exit")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[~ ERROR ~] Failed to grab frame")
                break

            writer.write(frame)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        stop_recording(writer)
        cap.release()
        cv2.destroyAllWindows()
        print(f"[~ DONE ~] Video saved successfully to {filepath}")


if __name__ == "__main__":
    main()