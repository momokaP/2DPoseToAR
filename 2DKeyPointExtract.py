import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2

# mediapipe KeyPoints
# https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker?hl=ko

def mediapipe_to_coco_keypoints(mp_keypoints, image_width, image_height):
    """
    mp_keypoints: np.array shape=(33,3), normalized (x,y,z)
    image_width, image_height: 영상 크기 (픽셀)
    
    반환: coco_keypoints 리스트 [x1,y1,c1,...,x17,y17,c17]
    """
    # MediaPipe → COCO 매핑 인덱스
    mp_to_coco_idx = [
        0,   # nose
        2,   # left_eye_inner (대체로 left_eye)
        5,   # right_eye_inner
        7,   # left_ear
        8,   # right_ear
        11,  # left_shoulder
        12,  # right_shoulder
        13,  # left_elbow
        14,  # right_elbow
        15,  # left_wrist
        16,  # right_wrist
        23,  # left_hip
        24,  # right_hip
        25,  # left_knee
        26,  # right_knee
        27,  # left_ankle
        28,  # right_ankle
    ]
    coco_keypoints = []
    for idx in mp_to_coco_idx:
        x_norm, y_norm, z = mp_keypoints[idx]
        # normalized 좌표를 픽셀 좌표로 변환
        x_px = x_norm * image_width
        y_px = y_norm * image_height
        # confidence (MediaPipe에선 없으므로 1로 고정)
        c = 1.0
        coco_keypoints.extend([x_px, y_px, c])
    return coco_keypoints


# 설정
SAVE_KEYPOINTS = True  # ← 저장 여부 설정
SAVE_PATH = "2d_keypoints_test.npy"
SAVE_PATH_COCO = "2d_keypoints_coco_test.npy"

# MediaPipe 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
cap = cv2.VideoCapture("video/dance2.mp4")

all_keypoints = []
all_keypoints_coco = []

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

        # COCO 포맷 변환
        h, w, _ = frame.shape
        coco_keypoints = mediapipe_to_coco_keypoints(keypoints, w, h)
        all_keypoints_coco.append(coco_keypoints)

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
    np.save(SAVE_PATH_COCO, all_keypoints_coco)
    print(f"Keypoints saved to {SAVE_PATH}")
