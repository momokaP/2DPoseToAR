# 2DtoAR
- 2DtoAR는 사람이 나오는 영상으로부터 3D 관절 좌표를 추출하고,
- 애니메이션이 적용된 3D 캐릭터를 AR로 보여줍니다.

# 주요 기능
- [mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=ko), [VideoPose3D](https://github.com/facebookresearch/VideoPose3D)를 이용하여 사람이 나오는 영상으로부터 3D 관절 좌표를 추출하여 .bvh 파일을 생성합니다.

  (.bvh 파일은 Biovision Hierarchy의 약자이며, 주로 모션 캡처 데이터를 저장하고, 캐릭터의 움직임을 재현하는 데 사용됩니다.)
![101](https://github.com/user-attachments/assets/e4fd8576-31ce-4a81-a800-1b3bed66c663)


- [panda3d](https://www.panda3d.org/)를 이용하여 애니메이션이 적용된 3D 캐릭터를 AR로 보여줍니다. (현재는 .gltf 파일만 가능합니다.)
![102](https://github.com/user-attachments/assets/e3f42eae-114d-402e-93c1-43380d808224)


- AR을 적용 할 때 필요한 카메라 정보과 체스보드 설정을 구할 수 있는 Calibration을 지원합니다.
![103](https://github.com/user-attachments/assets/f9091b34-de30-4932-83a7-2d56994701da)


# 설치 방법

사용한 라이브러리들

# 상세 기능
## 1. convert_video_to_bvh
#### 내부 동작
- (1) mediapipe를 이용하여 영상으로부터 2D 관절 키포인트를 추출한다.
- (2) 2D 관절 키포인트를 VideoPose3D에서 사용할 수 있는 형식으로 변환한다.
- (3) VideoPose3D를 사용하여 2D 관절 키포인트로부터 3D 관절 키포인트를 생성한다.
- (4) VideoPose3D가 생성한 3D 관절 키포인트를 .bvh 형식으로 변환한다.
 
#### 사용 방법
- 2DPoseToAR.py를 실행한다.
- '2d to .bvh' 탭을 선택하고, 포즈 영상 파일 경로를 선택한다.
![101](https://github.com/user-attachments/assets/bef0e53f-8a17-41a5-842f-6497b2e90a27)
![201](https://github.com/user-attachments/assets/63dde318-299a-4ef0-b2bc-2be13c00f01f)
- '영상에서 포즈 추출하고 .bvh로 변환' 버튼을 클릭한다.
- 2DPoseToAR.py와 같은 경로에서 생성된 .bvh 파일을 확인한다. (시간이 오래 걸린다...)
![202](https://github.com/user-attachments/assets/702d8aa0-ed3a-4a29-b096-2f216d4eeaaf)

#### .bvh 파일 이용하기
blender을 이용하여 .bvh 파일을 사용할 수 있다.

blender의 간단한 사용방법은 [how_to_use_blender.md](https://github.com/momokaP/2DPoseToAR/blob/main/how_to_use_blender.md)에 작성하였다.

## 2. show_ar


## 3. start_calibration

# 참고자료/reference

# 향후 개선 사항
