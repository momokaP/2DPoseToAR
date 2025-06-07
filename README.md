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

# 상세 기능
## 1. convert_video_to_bvh


## 2. show_ar


## 3. start_calibration

# 참고자료/reference

# 향후 개선 사항
