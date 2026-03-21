import os
import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QComboBox, QStatusBar, QSlider
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIcon, QFont

import tracker
from camera import detect_user_cams
from face_swap import initialize_model, load_target_face, swap_current_face
from logger import start_recording, write_frames, stop_recording
from tracker import draw_landmarks
from tracker import tracker_build, draw_landmarks

THEMES = {
    "Dark": """
        QMainWindow, QWidget {{
            background-color: #1a1a2e;
            color: #ccd6f6;
            font-family: Courier New;
            font-size: {font_size}px;
        }}
        QPushButton {{
            background-color: #112240;
            color: #64ffda;
            border: 1px solid #233554;
            border-radius: 6px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{ background-color: #233554; }}
        QLabel {{ color: #ffffff; }}
        QComboBox {{
            background-color: #112240;
            color: #ccd6f6;
            border: 1px solid #233554;
            border-radius: 6px;
            padding: 4px;
        }}
        QStatusBar {{ background-color: #112240; }}
    """,
    "Light": """
        QMainWindow, QWidget {{
            background-color: #f0f0f0;
            color: #1a1a2e;
            font-family: Courier New;
            font-size: {font_size}px;
        }}
        QPushButton {{
            background-color: #ffffff;
            color: #1d4ed8;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 4px;
        }}
        QStatusBar {{ color: #1d4ed8; background-color: #ffffff; }}
    """
}

class AlpaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alpa")
        self.setFixedSize(480, 620)
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.tracker = tracker_build()
        self.frame_count = 0
        self.last_tracked_frame = None

        self.app_model, self.swapper = None, None
        self.target_face = None #Issue?
        self.cap = None
        self.recording = False
        self.writer = None
        self.filepath = None
        self.font_size = 13
        self.frame_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()
        self.apply_theme("Dark")
        self.load_models()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        #Title
        title = QLabel("Alpa")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; letter-spacing: 8px;")
        layout.addWidget(title)

        subtitle = QLabel("by X3N0")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 20px; color: #8892b0;")
        layout.addWidget(subtitle)

        #Target face selection
        self.target_label = QLabel("No Target Selected!")
        self.target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.target_label)

        btn_browse = QPushButton("Select Target Face")
        btn_browse.clicked.connect(self.select_target)
        layout.addWidget(btn_browse)

        #Feed section
        self.feed_label = QLabel()
        self.feed_label.setFixedSize(440, 228)
        self.feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feed_label.setStyleSheet("border: 1px solid #233554;")
        self.feed_label.setText("Feed Not Started!")
        layout.addWidget(self.feed_label)

        self.feed_btn = QPushButton("Start Live Feed")
        self.feed_btn.clicked.connect(self.toggle_feed)
        layout.addWidget(self.feed_btn)

        self.rec_btn = QPushButton("Start Recording")
        self.rec_btn.clicked.connect(self.toggle_recording)
        layout.addWidget(self.rec_btn)

        #Apperance controls
        appearance = QHBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        appearance.addWidget(QLabel("Theme:"))
        appearance.addWidget(self.theme_combo)

        #Font
        font_layout = QHBoxLayout()

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Small", "Medium", "Large"])
        self.font_combo.currentTextChanged.connect(self.apply_font_size)
        font_layout.addWidget(QLabel("Font:"))
        font_layout.addWidget(self.font_combo)

        layout.addLayout(appearance)
        layout.addLayout(font_layout)

        #Stats bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("[~ IDLE ~] Waiting for input")


    def load_models(self):
        self.status.showMessage("[~ LOADING ~] Models")
        self.app_model, self.swapper = initialize_model()
        self.status.showMessage("[~ READY ~] Models loaded")

    def select_target(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Target Face", "",
            "Image Files (*.jpg *.jpeg *.png)"
        )
        if path:
            self.target_face = load_target_face(path, self.app_model)
            if self.target_face is not None:
                self.target_label.setText(f"Target: {path.split('/')[-1]}")
                self.status.showMessage("[~ READY ~] Target Face loaded")
            else:
                self.status.showMessage("[~ ERROR ~] No Face Detected In The Image")

    def toggle_feed(self):
        if self.timer.isActive():
            self.timer.stop()
            if self.cap:
                self.cap.release()
            self.feed_label.setText("Feed Stopped!")
            self.feed_btn.setText("Start Live Feed")
            self.status.showMessage("[~ IDLE ~] Feed Stopped")
        else:
            cams = detect_user_cams()
            if not cams:
                self.status.showMessage("[~ ERROR ~] No Cameras Detected")
                return
            os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
            self.cap = cv2.VideoCapture(cams[0], cv2.CAP_DSHOW)
            self.timer.start(10)
            self.feed_btn.setText("Stop Live Feed")
            self.status.showMessage("[~ LIVE ~] Feed Running")

    def update_frame(self):
        if not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            return

        self.frame_count += 1
        if self.frame_count % 3 == 0:
            self.last_tracked_frame = draw_landmarks(frame.copy(), self.tracker)
        if self.last_tracked_frame is not None:
            frame = self.last_tracked_frame

        if self.target_face is not None:
            frame = swap_current_face(frame, self.target_face, self.app_model, self.swapper)

        if self.recording and self.writer is not None:
            write_frames(self.writer, frame)

        #Convert OpenCV frame to Qt image for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qt_image = QImage(frame_rgb, w, h, ch * w, QImage.Format.Format_RGB888)
        self.feed_label.setPixmap(
            QPixmap.fromImage(qt_image).scaled(
                440, 248, Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def toggle_recording(self):
        if not self.recording:
            self.writer, self.filepath = start_recording()
            self.recording = True
            self.rec_btn.setText("Stop Recording")
            self.status.showMessage(f"[~ REC ~] Recording to {self.filepath}")
        else:
            stop_recording(self.writer)
            self.recording = False
            self.writer = None
            self.rec_btn.setText("Start Recording")
            self.status.showMessage(f"[~ SAVED ~] Recording Saved")


    def apply_font_size(self, size_name):
        #Map text options
        size_map = {
            "Small": 11,
            "Medium": 13,
            "Large": 16,
        }

        #Update font size var
        self.font_size = size_map.get(size_name, 13)
        self.apply_theme(self.theme_combo.currentText())#Refresh the current theme with new size

    def apply_theme(self, theme_name):
        style_template = THEMES.get(theme_name, THEMES["Dark"])

        #Inject the current font size into the theme selected
        final_style = style_template.format(font_size=self.font_size)
        self.setStyleSheet(final_style)

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        if self.recording and self.writer:
            stop_recording(self.writer)
        cv2.destroyAllWindows()
        event.accept()



def main():
        app = QApplication(sys.argv)
        window = AlpaWindow()
        window.show()
        sys.exit(app.exec())



if __name__ == "__main__":
    main()