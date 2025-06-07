import numpy as np

# 파일 로드
#data = np.load('./VideoPose3D/inference/output_directory/output.mp4.npz', allow_pickle=True)
# data = np.load('./VideoPose3D/data/data_2d_custom_myvideos.npz', allow_pickle=True)

#data = np.load('./my_video1234.npz', allow_pickle=True)
data = np.load('./VideoPose3D/data/data_2d_custom_myvideos1234.npz', allow_pickle=True)


# 키 확인
print("저장된 키 목록:")
print(data.files)

# 특정 키에 대한 데이터 보기
for key in data.files:
    print(f"\n키: {key}")
    print(f"타입: {type(data[key])}")
    print(f"내용 샘플:\n{data[key]}")


print("asdf")
print(data['positions_2d'].item()['my_video1234']['custom'][0].shape)  # 예: (300, 17, 2)

positions = data['positions_2d'].item()['my_video1234']['custom'][0]

import matplotlib.pyplot as plt
import cv2

video_path = './VideoPose3D/inference/input_directory/output.mp4'
cap = cv2.VideoCapture(video_path)

frame_idx = 10
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
ret, frame_img = cap.read()
cap.release()

if not ret:
    print("프레임을 불러올 수 없습니다.")
else:
    # BGR -> RGB 변환
    frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

    # 2. 키포인트 불러오기
    keypoints = data['positions_2d'].item()['my_video1234']['custom'][0][frame_idx]  # (17, 2)
    valid = ~np.any(np.isnan(keypoints), axis=1) & ~np.all(keypoints == 0, axis=1)

    # 3. 키포인트 표시
    plt.figure(figsize=(10, 6))
    plt.imshow(frame_img)
    plt.scatter(keypoints[valid, 0], keypoints[valid, 1], c='red', s=40)

    for i, (x, y) in zip(np.where(valid)[0], keypoints[valid]):
        plt.text(x + 5, y + 5, str(i), color='white', fontsize=8, bbox=dict(facecolor='black', alpha=0.5))

    plt.title("output.mp4 - Frame 10 with 2D Keypoints")
    plt.axis('off')
    plt.show()