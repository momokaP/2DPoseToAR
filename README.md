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
- 2DPoseToAR.py를 실행한다. (mediapipe의 import 시간이 길어서 어느정도 기다려야 창이 나온다.)
- '2d to .bvh' 탭을 선택하고, 포즈 영상 파일 경로를 선택한다.
![101](https://github.com/user-attachments/assets/bef0e53f-8a17-41a5-842f-6497b2e90a27)
![201](https://github.com/user-attachments/assets/63dde318-299a-4ef0-b2bc-2be13c00f01f)
- '영상에서 포즈 추출하고 .bvh로 변환' 버튼을 클릭한다.
- 2DPoseToAR.py와 같은 경로에서 생성된 .bvh 파일을 확인한다. (시간이 어느정도 걸린다.)
![202](https://github.com/user-attachments/assets/702d8aa0-ed3a-4a29-b096-2f216d4eeaaf)

#### .bvh 파일 이용하기
- .bvh 파일 편집 프로그램으로 blender가 필요하다.
- [blender 2.83](https://www.blender.org/download/releases/2-83/) 버전을 사용하였다. 

  (최신 버전의 blender는 .bvh 애니메이션이 적용된 캐릭터를 panda3d에서 불러올 때 문제가 생긴다.)
- (1) blender 프로그램을 실행하고 use_bvh.blend 파일을 연다. (use_bvh.blend 파일은 2DPoseToAR 폴더 내에 있다.)
![301](https://github.com/user-attachments/assets/5caafb6d-5982-48c4-85e3-28ed9b9b458e)
![302](https://github.com/user-attachments/assets/3b206279-ba2e-4659-86b2-b57b5578c7c4)

- (2) .bvh 파일을 import 한다. 여기서는 예시로 방금 만들었던 Deadlift~.bvh 파일을 사용한다.
![303](https://github.com/user-attachments/assets/699b1f0f-2c8b-4190-8293-e11ae26bd4cc)
![304](https://github.com/user-attachments/assets/f6b585b9-5f67-4e89-8d9f-eb5b14fd19de)

- (3) 블랜더 화면 아래를 보면 재생 버튼 같은 것이 보이고, 파란색으로 현재 애니메이션 프레임을 나타내는 것이 있는데, 현재 프레임을 마우스 드래그 하여 움직임을 관찰한다. 블랜더 화면의 왼쪽 위를 보면, 현재 프레임에 유효한 애니메이션이 있을 때 노란색으로 표시된다.
![305](https://github.com/user-attachments/assets/cfb0f904-95dc-4807-8d5f-2e135696435d)

- (4) 유효하지 않은 애니메이션이 있을 때 까지 프레임을 마우스 드래그 하여 움직이고, 그 때의 프레임 값을 End로 설정한다.
![306](https://github.com/user-attachments/assets/4951c5dd-fe06-4ba1-898c-5bb2137224bd)

- (5) 애니메이션 관절 2DtoAR
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
- 2DPoseToAR.py를 실행한다. (mediapipe의 import 시간이 길어서 어느정도 기다려야 창이 나온다.)
- '2d to .bvh' 탭을 선택하고, 포즈 영상 파일 경로를 선택한다.
![101](https://github.com/user-attachments/assets/bef0e53f-8a17-41a5-842f-6497b2e90a27)
![201](https://github.com/user-attachments/assets/63dde318-299a-4ef0-b2bc-2be13c00f01f)
- '영상에서 포즈 추출하고 .bvh로 변환' 버튼을 클릭한다.
- 2DPoseToAR.py와 같은 경로에서 생성된 .bvh 파일을 확인한다. (시간이 어느정도 걸린다.)
![202](https://github.com/user-attachments/assets/702d8aa0-ed3a-4a29-b096-2f216d4eeaaf)

#### .bvh 파일 이용하기
- .bvh 파일 편집 프로그램으로 blender가 필요하다.
- [blender 2.83](https://www.blender.org/download/releases/2-83/) 버전을 사용하였다. 

  (최신 버전의 blender는 .bvh 애니메이션이 적용된 캐릭터를 panda3d에서 불러올 때 문제가 생긴다.)
- (1) blender 프로그램을 실행하고 use_bvh.blend 파일을 연다. (use_bvh.blend 파일은 2DPoseToAR 폴더 내에 있다.)
![301](https://github.com/user-attachments/assets/5caafb6d-5982-48c4-85e3-28ed9b9b458e)
![302](https://github.com/user-attachments/assets/3b206279-ba2e-4659-86b2-b57b5578c7c4)

- (2) .bvh 파일을 import 한다. 여기서는 예시로 방금 만들었던 Deadlift~.bvh 파일을 사용한다.
![303](https://github.com/user-attachments/assets/699b1f0f-2c8b-4190-8293-e11ae26bd4cc)
![304](https://github.com/user-attachments/assets/f6b585b9-5f67-4e89-8d9f-eb5b14fd19de)

- (3) 블랜더 화면 아래를 보면 재생 버튼 같은 것이 보이고, 파란색으로 현재 애니메이션 프레임을 나타내는 것이 있는데, 현재 프레임을 마우스 드래그 하여 움직임을 관찰한다. 블랜더 화면의 왼쪽 위를 보면, 현재 프레임에 유효한 애니메이션이 있을 때 노란색으로 표시된다.
![305](https://github.com/user-attachments/assets/cfb0f904-95dc-4807-8d5f-2e135696435d)

- (4) 유효하지 않은 애니메이션이 있을 때까지 프레임을 마우스 드래그 하여 움직이고, 그 때의 프레임 값을 End로 설정한다.
![306](https://github.com/user-attachments/assets/4951c5dd-fe06-4ba1-898c-5bb2137224bd)

- (5) 애니메이션 관절을 선택하고 블랜더 화면 오른쪽의 사람 모양의 아이콘(object data properties)을 클릭한 뒤, Rest Position을 클릭하여 미리 설정해 놓은 캐릭터와 같은 자세가 되도록 한다. 이후 캐릭터와 애니메이션 관절은 모두 선택하고, ctrl + p를 누른 뒤, Armature Deform의 With Automatic Weights를 클릭한다.
![307](https://github.com/user-attachments/assets/a64bb26c-0e72-421b-95bf-0319d8553888)
![308](https://github.com/user-attachments/assets/4f6d81b6-91e8-4fc1-9b4e-3c731b2c5f75)


-

## 2. show_ar


## 3. start_calibration

# 참고자료/reference

# 향후 개선 사항
