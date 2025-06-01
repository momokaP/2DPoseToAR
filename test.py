import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
cap = cv2.VideoCapture("moving.mp4")

all_keypoints = []

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark])
    else:
        keypoints = np.zeros((33, 3))  # 33개 관절, 못 찾은 경우 0으로 채움

    all_keypoints.append(keypoints)

cap.release()
np.save("2d_keypoints.npy", all_keypoints)
