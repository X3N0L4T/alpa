import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def tracker_build():
    return mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=False, #Change True or False to remove extra points
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


def draw_landmarks(frame, tracker, draw_mesh=True):
    small = cv2.resize(frame, (320, 240)) #process at half size
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    results = tracker.process(rgb)

    if not results.multi_face_landmarks:
        return frame #orginal

    for face_landmarks in results.multi_face_landmarks:
        if draw_mesh:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
        )
    return frame

def get_landmarks(frame, tracker):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = tracker.process(rgb)

    if not results.multi_face_landmarks:
        return []

    h, w = frame.shape[:2]
    points = []
    for face_landmarks in results.multi_face_landmarks:
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x,y))
    return points


def main():
    tracker = tracker_build()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("[~ ERROR ~] Empty frame.")
            break

        frame = draw_landmarks(frame, tracker)
        cv2.imshow("Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Clean
    cap.release()
    cv2.destroyAllWindows()
    tracker.close()




if __name__ == '__main__':
    main()