import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2

# 설정
SAVE_KEYPOINTS = True  # ← 저장 여부 설정
SAVE_PATH = "2d_keypoints_test.npy"

# MediaPipe 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
cap = cv2.VideoCapture("video/dance2.mp4")

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
        keypoints = np.zeros((33, 3))  # 관절 인식 실패 시 0

    if SAVE_KEYPOINTS:
        all_keypoints.append(keypoints)

    # 시각화용 랜드마크 리스트 생성
    landmarks = []
    for kp in keypoints:
        lm = landmark_pb2.NormalizedLandmark()
        lm.x, lm.y, lm.z = float(kp[0]), float(kp[1]), float(kp[2])
        landmarks.append(lm)

    landmark_list = landmark_pb2.NormalizedLandmarkList(landmark=landmarks)

    # 시각화
    mp_drawing.draw_landmarks(
        frame,
        landmark_list,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )

    cv2.imshow("Pose Visualization", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# 저장 옵션
if SAVE_KEYPOINTS:
    np.save(SAVE_PATH, all_keypoints)
    print(f"Keypoints saved to {SAVE_PATH}")
