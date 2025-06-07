import cv2
import mediapipe as mp
import numpy as np
import os
import sys
from glob import glob
import argparse
import subprocess


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

    dummy = [0.0] * len(x)  # dummy

    return np.array([x, y, dummy, conf], dtype=np.float32)

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

            # key points
            keypoint_frame = mediapipe_to_coco_keypoints(landmarks, frame_width, frame_height)
            frame_keypoints = [[], np.array([keypoint_frame])]

            # bounding box
            x_min, x_max = keypoint_frame[0].min(), keypoint_frame[0].max()
            y_min, y_max = keypoint_frame[1].min(), keypoint_frame[1].max()
            score_mean = np.mean(keypoint_frame[3])
            box = np.array([[x_min, y_min, x_max, y_max, score_mean]], dtype=np.float32)
            frame_boxes = [[], box]
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
    video = './video/dance1.mp4'
    output = 'dance1.npz'

    boxes, keypoints, segments, metadata = extract_keypoints_and_boxes(video)
    save_to_npz(output, boxes, keypoints, segments, metadata)

    #############################################
    #############################################

    # 현재 파일 기준으로 VideoPose3D/data 경로 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'VideoPose3D', 'data')
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    from prepare_data_2d_custom import decode
    from prepare_data_2d_custom import output_prefix_2d
    from data_utils import suggest_metadata

    input_file = output #'/absolute/path/to/your/file.npz'     # 1개의 .npz 파일
    output_suffix = 'dance1'                # 출력 파일 이름 접미사

    if not os.path.isfile(input_file):
        print(f'[ERROR] 입력 파일이 존재하지 않습니다: {input_file}')
        exit(1)

    print('Parsing 2D detections from:', input_file)

    metadata = suggest_metadata('coco')
    metadata['video_metadata'] = {}

    canonical_name = os.path.splitext(os.path.basename(input_file))[0]
    data, video_metadata = decode(input_file)

    output = {
        canonical_name: {
            'custom': [data[0]['keypoints'].astype('float32')]
        }
    }
    metadata['video_metadata'][canonical_name] = video_metadata

    print('Saving...')
    np.savez_compressed(output_prefix_2d + output_suffix, positions_2d=output, metadata=metadata)
    print(f'Done. Saved to {output_prefix_2d + output_suffix}')

    #############################################
    #############################################

    runpy_dir = os.path.join(current_dir, 'VideoPose3D')
    # runpy_dir = '/absolute/path/to/VideoPose3D'  # run.py가 있는 폴더
    output_video = 'dance1.mp4'
    output_positions = 'dance1'

    # 명령어를 문자열 리스트로 구성
    cmd = [
        'python', 'run.py', # 고정
        '--datapath', current_dir,
        '-d', 'custom', # 고정
        '-k', output_suffix,
        '-arc', '3,3,3,3,3',
        '-c', 'checkpoint', # 고정
        '--evaluate', 'pretrained_h36m_detectron_coco.bin', # 고정
        '--render', # 고정
        '--viz-subject', 'dance1',
        '--viz-action', 'custom', # 고정
        '--viz-camera', '0', # 고정
        '--viz-output', os.path.join(current_dir, output_video),
        '--viz-export', os.path.join(current_dir, output_positions),
        '--viz-size', '6',
    ]

    # 실행
    subprocess.run(cmd, cwd=runpy_dir)