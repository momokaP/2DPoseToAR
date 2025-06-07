import numpy as np
import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2  # 직접 import

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

keypoints = np.load("2d_keypoints.npy")  # (frame, 33, 3)
cap = cv2.VideoCapture("video/moving.mp4")

i = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret or i >= len(keypoints):
        break

    # NormalizedLandmark 객체 생성
    landmarks = []
    for kp in keypoints[i]:
        landmark = landmark_pb2.NormalizedLandmark()
        landmark.x = float(kp[0])
        landmark.y = float(kp[1])
        landmark.z = 0.0
        landmarks.append(landmark)

    landmark_list = landmark_pb2.NormalizedLandmarkList(landmark=landmarks)

    # 시각화
    mp_drawing.draw_landmarks(
        frame,
        landmark_list,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )

    cv2.imshow("Pose", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    i += 1

cap.release()
cv2.destroyAllWindows()
