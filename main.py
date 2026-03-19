import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

from camera import detect_user_cams
from face_swap import initialize_model, load_target_face, swap_current_face
from logger import start_recording, write_frames, stop_recording


app, swapper = None, None
target_face = None
recording = False
writer = None
filepath = None

def load_model_on_start():
    global app, swapper
    print("[~ ALPA ~] Loading models...")
    app, swapper = initialize_model()


def select_target_image(label):
    global target_face
    path = filedialog.askopenfilename(
        title="Select Target Face",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if path:
        target_face = load_target_face(path, app)
        if target_face is not None:
            label.config(text=f"Target: {path.split('/')[-1]}")
        else:
            messagebox.showerror("Error", "No face detected in selected image")


def toggle_recording(btn):
    global recording, writer, filepath
    if not recording:
        writer, filepath = start_recording()
        if writer:
            recording = True
            btn.config(text="STOP RECORDING", fg="red")
            print(f"[~ INFO ~] Recording started: {filepath}")
    else:
        stop_recording(writer)
        recording = False
        writer = None
        btn.config(text="START RECORDING", fg="black")
        print(f"[~ INFO ~] Recording stopped and saved: {filepath}")


def run_feed(window):
    global target_face, recording, writer

    cams = detect_user_cams()
    if not cams:
        messagebox.showerror("Error", "No cameras found")
        return

    cap = cv2.VideoCapture(cams[0])
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera")
        return

    def update_frame():
        global recording, writer
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return

        if target_face is not None:
            frame = swap_current_face(frame, target_face, app, swapper)

        if recording and writer is not None:
            write_frames(writer, frame)

        cv2.imshow("Alpa - Live Feed", frame)
        cv2.waitKey(1)

        window.after(10, update_frame)

    update_frame()


def build_gui():
    window = tk.Tk()
    window.title("Alpa - Identity Synthesis Demo")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(
        window,
        text="ALPA",
        font=("Courier", 24, "bold")
    ).pack(pady=10)

    tk.Label(
        window,
        text="Real-Time Identity Synthesis Demo",
        font=("Courier", 10)
    ).pack()

    target_label = tk.Label(window, text="No target selected", font=("Courier", 9))
    target_label.pack(pady=5)

    tk.Button(
        window,
        text="Select Target Face",
        command=lambda: select_target_image(target_label)
    ).pack(pady=5)

    tk.Button(
        window,
        text="Start Live Feed",
        command=lambda: run_feed(window)
    ).pack(pady=5)

    rec_btn = tk.Button(
        window,
        text="Start Recording",
        width=25
    )

    rec_btn.config(command=lambda: toggle_recording(rec_btn))
    rec_btn.pack(pady=5)

    tk.Button(
        window,
        text="Exit",
        width=25,
        fg="white",
        bg="red",
        command=window.destroy
    ).pack(pady=20)

    window.mainloop()


def main():
    load_model_on_start()
    build_gui()


if __name__ == "__main__":
    main()