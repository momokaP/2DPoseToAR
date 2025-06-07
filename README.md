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

## 2. show_AR
- show_AR은 애니메이션이 적용된 gltf 형식의 3D 캐릭터를 현실의 영상에 보여주는 기능을 한다.
#### 사용 방법
- 2DPoseToAR.py를 실행하고 'show AR' 탭을 선택한다.

![102](https://github.com/user-attachments/assets/62b0d6b8-fbc4-42a1-8a48-3f422f6fc371)
- gltf 파일, 영상 파일, 카메라 체스보드 설정 파일, 애니메이션 이름을 입력한 뒤 'AR로 보여주기' 버튼을 누르면 AR이 적용된 영상이 나온다.

![401](https://github.com/user-attachments/assets/0e94c36b-a944-47bc-9e97-f3a5d6c44b19)
- 영상은 calibration을 적용하기 위한 체스보드가 있어야 한다.
- 카메라 체스보드 설정 파일의 내용은 다음과 같다. 카메라 체스보드의 설정 내용은 Calibration을 통해 구할 수 있다.
```
K=[[659.81531748, 0.00000000, 634.27502575], [0.00000000, 675.89216586, 399.59526493], [0.00000000, 0.00000000, 1.00000000]]
dist_coeff=[0.009225288073331894, 0.11877838871914687, -0.008850057927963083, 0.0077549737755990686, -0.1617903747491421]
board_pattern=(10,7)
board_cellsize=0.020
```
- 애니메이션 이름은 gltf파일에 있는 애니메이션 이름과 동일해야 한다.

![333](https://github.com/user-attachments/assets/dda9c634-a05a-45cf-a409-06dcdf9b702a)

(blender에서 import 한 gltf 파일의 예)

## 3. Calibration
- Calibration은 show_AR에서 입력되는 카메라 체스보드 설정 파일의 내용을 구하기 위해 사용할 수 있다.
- [https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py](https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py)의 코드를 사용하였다.

#### 사용 방법
- Calibration을 위한 체스보드를 준비한다. [Calibration Checkerboard Collection](https://markhedleyjones.com/projects/calibration-checkerboard-collection)에서 체스보드를 구할 수 있다.
- Calibration을 위한 체스보드가 포함된 영상을 촬영한다.
- 2DPoseToAR.py를 실행하고 'Calibration을' 탭을 선택한다.

![103](https://github.com/user-attachments/assets/2479838f-d66f-466c-8742-d6a1bea94925)

- 촬영한 영상 파일을 입력하고, 체스보드 패턴 (colsxrows), 보드 셀 크기를 입력한다.

  체스보드 패턴은 체스보드의 교차점을 기준으로 한다.

  ![asdf](https://github.com/user-attachments/assets/eeb7e943-75ca-457e-8ba4-83909c03eecd)

  이와 같은 경우에 가로 8, 세로 6 이다.

  보드 셀 크기는 교자점 사이의 거리를 미터 단위로 나타낸 것이다.

- '캘리브레이션 시작' 버튼을 누르면 영상이 나오는데,

  스페이스 바를 누르면 영상이 멈추고, 체스보드의 교차점에 점이 표시된다.

  ![402](https://github.com/user-attachments/assets/b48e41dc-13da-4e07-bbc4-54743192bf69)

  이 상태에서 엔터를 누르면 해당 이미지가 선택된다. 선택된 이미지들을 기반으로 캘리브레이션이 수행된다.

  ![403](https://github.com/user-attachments/assets/f31d7c3a-ac97-474e-af9c-ce38a0fc3cd3)

- Esc를 누르면 영상이 종료되고,  영상 이름에 접미사로 _calibration_result.txt가 붙은 파일이 2DPoseToAR.py와의 같은 경로에 생성된다. 파일 내용은 다음과 같은 형식이다.
```
## Camera Calibration Results
* The number of selected images = 1
* RMS error = 0.726244
* Camera matrix (K) = [[904.37506382, 0.00000000, 678.53835620], [0.00000000, 766.68651170, 435.66893130], [0.00000000, 0.00000000, 1.00000000]]
* Distortion coefficient (k1, k2, p1, p2, k3, ...) = [0.02402269049495, -0.5647570185067435, 0.013773852263923648, 0.018542707176849228, 2.7222135346360252]
* board_pattern = (10, 7)
* board_cellsize = 0.023
```
  이 파일의 내용으로 show_AR에서 입력되는 카메라 체스보드 설정 파일의 내용을 만든다.
```
K=[[904.37506382, 0.00000000, 678.53835620], [0.00000000, 766.68651170, 435.66893130], [0.00000000, 0.00000000, 1.00000000]]
dist_coeff=[0.02402269049495, -0.5647570185067435, 0.013773852263923648, 0.018542707176849228, 2.7222135346360252]
board_pattern=(10, 7)
board_cellsize=0.023
```

# 참고자료/reference

# 향후 개선 사항
