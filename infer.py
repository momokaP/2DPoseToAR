import cv2
import mediapipe as mp
import numpy as np

def mediapipe_to_coco_keypoints(mp_landmarks, image_width, image_height):
    # MediaPipe → COCO 매핑 인덱스
    mp_to_coco_idx = [
        0,   # nose
        2,   # left eye
        5,   # right eye
        7,   # left ear
        8,   # right ear
        11,  # left shoulder
        12,  # right shoulder
        13,  # left elbow
        14,  # right elbow
        15,  # left wrist
        16,  # right wrist
        23,  # left hip
        24,  # right hip
        25,  # left knee
        26,  # right knee
        27,  # left ankle
        28,  # right ankle
    ]

    x = []
    y = []
    conf = []
    for idx in mp_to_coco_idx:
        l = mp_landmarks[idx]
        x.append(l.x * image_width)
        y.append(l.y * image_height)
        conf.append(l.visibility)  # 신뢰도

    dummy = [0.0] * len(x)  # dummy Z 또는 logit

    return np.array([x, y, dummy, conf], dtype=np.float32)  # shape: (4, 17)

def extract_keypoints_and_boxes(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(video_path)
    boxes, keypoints, segments = [], [], []

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_idx = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        frame_boxes = []
        frame_keypoints = []

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            keypoint_frame = mediapipe_to_coco_keypoints(landmarks, frame_width, frame_height)
            frame_keypoints = [[], np.array([keypoint_frame])]
            #frame_keypoints = [[], keypoint_frame]  # shape: (1, 4, 17)

            # bounding box 계산
            x_min, x_max = keypoint_frame[0].min(), keypoint_frame[0].max()
            y_min, y_max = keypoint_frame[1].min(), keypoint_frame[1].max()
            score_mean = np.mean(keypoint_frame[3])
            box = np.array([[x_min, y_min, x_max, y_max, score_mean]], dtype=np.float32)
            frame_boxes = [[], box]

            # # keypoints: [x, y, dummy, score]
            # x_coords = np.array([l.x * frame_width for l in landmarks], dtype=np.float32)
            # y_coords = np.array([l.y * frame_height for l in landmarks], dtype=np.float32)
            # scores = np.array([l.visibility for l in landmarks], dtype=np.float32)

            # dummy = np.zeros_like(scores)

            # keypoint_frame = np.stack([x_coords, y_coords, dummy, scores], axis=0)
            # frame_keypoints = [keypoint_frame]  # shape: (1, 4, N)
            
            # # bounding box [x1, y1, x2, y2, confidence]
            # x_min, x_max = x_coords.min(), x_coords.max()
            # y_min, y_max = y_coords.min(), y_coords.max()
            # box = np.array([[x_min, y_min, x_max, y_max, scores.mean()]], dtype=np.float32)
            # frame_boxes = [[], box]  # mimic Detectron2 format

        else:
            frame_keypoints = [[], []]
            frame_boxes = [[], []]

        boxes.append(frame_boxes)
        keypoints.append(frame_keypoints)
        segments.append(None)
        frame_idx += 1

    cap.release()
    return boxes, keypoints, segments, {'w': frame_width, 'h': frame_height}


def save_to_npz(out_path, boxes, keypoints, segments, metadata):
    np.savez_compressed(
        out_path,
        boxes=np.array(boxes, dtype=object),
        keypoints=np.array(keypoints, dtype=object),
        segments=segments,
        metadata=metadata
    )


if __name__ == "__main__":
    video = './VideoPose3D/inference/input_directory/output.mp4'
    output = 'my_video1234.npz'

    boxes, keypoints, segments, metadata = extract_keypoints_and_boxes(video)
    save_to_npz(output, boxes, keypoints, segments, metadata)
