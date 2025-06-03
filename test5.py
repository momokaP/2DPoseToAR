import numpy as np

# 파일 불러오기
data = np.load('output.npy')  # 실제 파일 이름에 맞게 변경하세요

# 구조 출력
print("Shape:", data.shape)
print("Dtype:", data.dtype)

# 첫 프레임, 첫 관절 확인
print("\nFirst frame, first joint:", data[0, 0])  # shape: (프레임 수, 관절 수, 3)

# 예시로 처음 몇 개 프레임 출력
print("\nFirst 3 frames:\n", data[:3])