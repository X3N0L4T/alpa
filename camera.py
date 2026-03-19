import cv2

def detect_user_cams(max_allow=5):
    """Returns a list of available cameras"""
    available_cams = []

    for index in range(max_allow):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            available_cams.append(index)
            cap.release()

    return available_cams


def get_frames(cam_index):
    cap = cv2.VideoCapture(cam_index)

    if not cap.isOpened():
        print(f"[~ ERROR ~] Could not open camera {cam_index}")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"[~ ERROR ~] Failed to read frame")
        return None

    return frame


def main():
    available_cams = detect_user_cams()
    print(f"[~ INFO ~] Found {len(available_cams)} cameras")

    if not available_cams:
        print("[~ ERROR ~] No available cameras, please check your connection")
        return

    cap = cv2.VideoCapture(available_cams[0])

    print(f"Press 'q' to exit the live feed")
    while True:
        ret, frame = cap.read()

        if not ret:
            print(f"[~ ERROR ~] Failed to grab frame")
            break

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()