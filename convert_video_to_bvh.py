import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import subprocess

from bvh_skeleton import h36m_skeleton

def write_standard_bvh(outbvhfilepath, prediction3dpoint):
    # https://github.com/HW140701/VideoTo3dPoseAndBvh/tree/master의 코드 사용.
    # https://github.com/HW140701/VideoTo3dPoseAndBvh/blob/master/videopose.py line 263.

    # https://github.com/HW140701/VideoTo3dPoseAndBvh/tree/master/bvh_skeleton의 코드들 import 사용.

    '''
    :param outbvhfilepath: 원본 비디오 경로 또는 그와 동일한 경로 형식 (예: "/path/to/video.mp4")
    :param prediction3dpoint: 예측된 3D 관절 좌표 (프레임 수 x 관절 수 x 3)
    '''

    # 1. 좌표를 100배 (미터 → 센티미터)
    for frame in prediction3dpoint:
        for point3d in frame:
            point3d[0] *= 100
            point3d[1] *= 100
            point3d[2] *= 100

    # 2. 출력 파일 경로 계산: 확장자만 `.bvh`로 교체
    dir_name = os.path.dirname(outbvhfilepath)
    basename = os.path.basename(outbvhfilepath)
    video_name = os.path.splitext(basename)[0]  # "video" ← "video.mp4"

    bvhfilePath = os.path.join(dir_name, f"{video_name}.bvh")

    # 3. 디렉토리 없으면 생성
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 4. BVH 생성
    human36m_skeleton = h36m_skeleton.H36mSkeleton()
    human36m_skeleton.poses2bvh(prediction3dpoint, output_file=bvhfilePath)

def save_to_npz(out_path, boxes, keypoints, segments, metadata):
    np.savez_compressed(
        out_path,
        boxes=np.array(boxes, dtype=object),
        keypoints=np.array(keypoints, dtype=object),
        segments=segments,
        metadata=metadata
    )

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

def Format_Conversion(__file__, output, suffix):
    # 현재 파일 기준으로 VideoPose3D/data 경로 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'VideoPose3D', 'data')
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    from prepare_data_2d_custom import decode
    from prepare_data_2d_custom import output_prefix_2d
    from data_utils import suggest_metadata

    input_file = output # .npz 파일
    output_suffix = suffix # 출력 파일 이름 접미사

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
    return current_dir, output_suffix

def Make_3D_KeyPoint(suffix, output_positions, current_dir, output_suffix):
    runpy_dir = os.path.join(current_dir, 'VideoPose3D')  

    # 명령어를 문자열 리스트로 구성
    cmd = [
        'python', 'run.py', # 고정
        '--datapath', current_dir,
        '-d', 'custom', # 고정
        '-k', output_suffix,
        '-arc', '3,3,3,3,3', # 고정?
        '-c', 'checkpoint', # 고정
        '--evaluate', 'pretrained_h36m_detectron_coco.bin', # 고정
        '--render', # 고정
        '--viz-subject', suffix, 
        '--viz-action', 'custom', # 고정
        '--viz-camera', '0', # 고정
        '--viz-export', os.path.join(current_dir, output_positions),
        '--viz-size', '6', # 고정?
    ]

    # 실행
    subprocess.run(cmd, cwd=runpy_dir)

    return os.path.join(current_dir, output_positions)

def process_video_to_bvh(video_path):
    """
    비디오 파일을 입력받아 Mediapipe로 2D 키포인트를 추출하고,
    이를 VideoPose3D로 3D 키포인트로 변환한 뒤, .bvh 파일로 저장하는 전체 파이프라인을 실행합니다.

    Parameters:
        video_path (str): 입력 비디오 경로

    Returns:
        str: 생성된 .bvh 파일 경로
    """

    # video = './video/dance1.mp4'
    # output = 'dance1.npz'
    # suffix = 'dance1'
    # output_positions = 'dance1'

    # ex) video_path = './video/dance1.mp4'
    filename_with_ext = os.path.basename(video_path)   # 'dance1.mp4'
    filename_without_ext = os.path.splitext(filename_with_ext)[0]  # 'dance1'

    output_npz_path = filename_without_ext + '.npz'
    suffix = filename_without_ext
    output_positions_prefix = filename_without_ext

    # 1. Mediapipe를 사용해서 영상에서 2D 키포인트 추출
    boxes, keypoints, segments, metadata = extract_keypoints_and_boxes(video_path)
    save_to_npz(output_npz_path, boxes, keypoints, segments, metadata)

    # 2. VideoPose3D에서 사용할 수 있는 형식으로 변환
    current_dir, output_suffix = Format_Conversion(__file__, output_npz_path, suffix)

    # 3. VideoPose3D로 2D 키포인트를 3D로 예측
    output_positions = Make_3D_KeyPoint(suffix, output_positions_prefix, current_dir, output_suffix)

    # 4. 3D 키포인트를 .bvh 포맷으로 변환
    prediction3dpoint = np.load(output_positions + '.npy')
    out_path = output_positions
    write_standard_bvh(out_path, prediction3dpoint)

    return out_path + '.bvh'

