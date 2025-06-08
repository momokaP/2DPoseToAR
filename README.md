# 2DtoAR
- 2DtoAR는 사람이 나오는 영상으로부터 3D 관절 좌표를 추출하고,
- 애니메이션이 적용된 3D 캐릭터를 AR로 보여줍니다.
- BVHConverter.py, ARCalib.py 파일을 통하여 기능을 제공합니다.

https://github.com/user-attachments/assets/02e9fef5-e99a-49d6-b55c-15709aeda32d

이 운동 영상을 이용하여 3D 관절 좌표를 추출하고,

https://github.com/user-attachments/assets/2ac206f4-ceba-49d7-815c-14fb3a0f2bca

애니메이션이 적용된 3D 캐릭터를 AR로 보여줍니다.

# 주요 기능
- [mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=ko), [VideoPose3D](https://github.com/facebookresearch/VideoPose3D)를 이용하여 사람이 나오는 영상으로부터 3D 관절 좌표를 추출하여 .bvh 파일을 생성합니다.

  (.bvh 파일은 Biovision Hierarchy의 약자이며, 주로 모션 캡처 데이터를 저장하고, 캐릭터의 움직임을 재현하는 데 사용됩니다.)
  
![111](https://github.com/user-attachments/assets/24d6ce50-f767-46a1-8d6f-ecaed1beeb47)

- [panda3d](https://www.panda3d.org/)를 이용하여 애니메이션이 적용된 3D 캐릭터를 AR로 보여줍니다. (현재는 .gltf 파일만 가능합니다.)
  
![112](https://github.com/user-attachments/assets/ce0acf94-597b-461e-849f-3d87e8311fa0)

- AR을 적용 할 때 필요한 카메라 정보과 체스보드 설정을 구할 수 있는 Calibration을 지원합니다.

![113](https://github.com/user-attachments/assets/7c29e9a9-10ff-45ed-8b7f-d0dae213a70c)

# 설치 방법

1. 2DPoseToAR을 Clone 하거나 zip 파일을 다운 받는다.

2. 필요한 라이브러리들을 설치한다.
   실행 당시 파이썬 버전 Python 3.11.5

   사용한 라이브러리들 cv2(opencv-contrib-python, 4.11.0.86), numpy(1.26.4), mediapipe(0.10.18)

   (Python 3.13 이상인 경우에 mediapipe 설치가 안된다. Python 3.10을 권장한다.)

   ```
   pip install opencv-contrib-python
   pip install mediapipe
   ```
4. panda3d를 설치한다.
   [https://www.panda3d.org/](https://www.panda3d.org/)에서 SDK를 설치하고,
   파이썬에서 pip install panda3d 으로 panda3d를 설치한다.

5. BVHConverter.py 또는 ARCalib.py를 실행한다.


# 상세 기능
## 1. BVH Converter
#### 내부 동작
- (1) mediapipe를 이용하여 영상으로부터 2D 관절 키포인트를 추출한다.
- (2) 2D 관절 키포인트를 VideoPose3D에서 사용할 수 있는 형식으로 변환한다.
- (3) VideoPose3D를 사용하여 2D 관절 키포인트로부터 3D 관절 키포인트를 생성한다.
- (4) VideoPose3D가 생성한 3D 관절 키포인트를 .bvh 형식으로 변환한다.
 
#### 사용 방법
- BVHConverter.py를 실행하고 포즈 영상 파일 경로를 선택한다.

- (mediapipe를 import 할때 시간이 오래 걸려서 실행 시간이 오래 걸린다.)

![111](https://github.com/user-attachments/assets/e60c608e-6dd1-425b-939a-79e43729c051)

![221](https://github.com/user-attachments/assets/8ba1d054-9469-43a8-a968-b5715b3fc59e)

- '영상에서 포즈 추출하고 .bvh로 변환' 버튼을 클릭한다.
- BVHConverter.py와 같은 경로에서 생성된 .bvh 파일을 확인한다.

  (시간이 오래 걸린다.)

![222](https://github.com/user-attachments/assets/21aac3ed-1346-477c-a055-32dd56e4e97d)

#### .bvh 파일 이용하기
blender을 이용하여 .bvh 파일을 사용할 수 있다.

blender의 간단한 사용방법은 [how_to_use_blender.md](https://github.com/momokaP/2DPoseToAR/blob/main/how_to_use_blender.md)에 작성하였다.

## 2. ARCalib - Show_AR
- Show_AR은 애니메이션이 적용된 gltf 형식의 3D 캐릭터를 현실의 영상에 보여주는 기능을 한다.
#### 사용 방법
- ARCalib.py를 실행하고 'Show AR' 탭을 선택한다.

![112](https://github.com/user-attachments/assets/d1f38c7c-f4e7-43c3-a6d9-8bde398442df)

- gltf 파일, 영상 파일, 카메라 체스보드 설정 파일, 애니메이션 이름을 입력한 뒤 'AR로 보여주기' 버튼을 누르면 AR이 적용된 영상이 나온다.

![441](https://github.com/user-attachments/assets/26598130-7e0b-467b-a450-03be06350011)

![442](https://github.com/user-attachments/assets/1c450475-f691-48c2-95e2-d9cbfdf2cf41)

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

- AR이 적용된 영상에서 a, s, d, f 키로 캐릭터를 xy평면에 대해 이동 시킬 수 있고, q, e 키를 이용하여 z축 기준으로 회전시킬 수 있다.

  o, p 키를 이용하여 캐릭터의 크기를 조절할 수 있으며, r 키를 이용하여 원래의 위치, 회전, 크기으로 되돌릴 수 있다.

  스페이스 바를 이용하여 영상의 재생, 정지가 가능하다.

## 3. Calibration
- Calibration은 show_AR에서 입력되는 카메라 체스보드 설정 파일의 내용을 구하기 위해 사용할 수 있다.
- [https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py](https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py)의 코드를 사용하였다.

#### 사용 방법
- Calibration을 위한 체스보드를 준비한다. [Calibration Checkerboard Collection](https://markhedleyjones.com/projects/calibration-checkerboard-collection)에서 체스보드를 구할 수 있다.
- Calibration을 위한 체스보드가 포함된 영상을 촬영한다.
- 2ARCalib.py를 실행하고 'Calibration을' 탭을 선택한다.

![113](https://github.com/user-attachments/assets/be6cf71f-204e-41ca-b64c-74abe774c02a)

- 촬영한 영상 파일을 입력하고, 체스보드 패턴 (cols x rows), 보드 셀 크기를 입력한다.

  체스보드 패턴은 체스보드의 교차점을 기준으로 한다.

  ![asdf](https://github.com/user-attachments/assets/eeb7e943-75ca-457e-8ba4-83909c03eecd)

  이와 같은 경우에 가로 8, 세로 6 이다.

  보드 셀 크기는 교자점 사이의 거리를 미터 단위로 나타낸 것이다.

- '캘리브레이션 시작' 버튼을 누르면 영상이 나오는데,

  스페이스 바를 누르면 영상이 멈추고, 체스보드의 교차점에 점이 표시된다.

  ![402](https://github.com/user-attachments/assets/b48e41dc-13da-4e07-bbc4-54743192bf69)

  이 상태에서 엔터를 누르면 해당 이미지가 선택된다. 선택된 이미지들을 기반으로 캘리브레이션이 수행된다.

  ![403](https://github.com/user-attachments/assets/f31d7c3a-ac97-474e-af9c-ce38a0fc3cd3)

- Esc를 누르면 영상이 종료되고,  영상 이름에 접미사로 _calibration_result.txt가 붙은 파일이 ARCalib.py와의 같은 경로에 생성된다. 파일 내용은 다음과 같은 형식이다.
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

# 시연 영상

https://github.com/user-attachments/assets/adac9ac1-5cd0-4454-9e9d-bc8047bf853c

https://github.com/user-attachments/assets/b3381f36-f340-478e-a771-86b99e970c46

# 참고자료/reference
[mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=ko)의 기능을 사용하였다.

[VideoPose3D](https://github.com/facebookresearch/VideoPose3D)의 코드 일부를 수정, 참고하여 사용하였다.
([convert_video_to_bvh.py](https://github.com/momokaP/2DPoseToAR/blob/main/convert_video_to_bvh.py)의 Format_Conversion 함수)

[VideoTo3dPoseAndBvh](https://github.com/HW140701/VideoTo3dPoseAndBvh/tree/master)의 코드를 참고하여 사용하였다.
[bvh_skeleton](https://github.com/HW140701/VideoTo3dPoseAndBvh/tree/master/bvh_skeleton)의 일부 코드들을 import 하였고,
[videopose.py](https://github.com/HW140701/VideoTo3dPoseAndBvh/blob/master/videopose.py)를 참고하여 [convert_video_to_bvh.py](https://github.com/momokaP/2DPoseToAR/blob/main/convert_video_to_bvh.py)의 write_standard_bvh 함수를 작성하였다.

[Visual-Copmuting](https://github.com/tgt5248/Visual-Copmuting/tree/main)의 코드를 참고하였다.
[panda3d.py](https://github.com/tgt5248/Visual-Copmuting/blob/main/Ar_application/panda3d.py)의 코드를 참고하여
[show_ar.py](https://github.com/momokaP/2DPoseToAR/blob/main/show_ar.py)를 작성하였다.

[https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py](https://github.com/mint-lab/3dv_tutorial/blob/master/examples/camera_calibration.py)의 코드를 참고하여 [Camera_Calibration.py](https://github.com/momokaP/2DPoseToAR/blob/main/Camera_Calibration.py)을 작성하였다.

본 프로젝트에서 쓰인 영상은

Squat.mp4
[https://commons.wikimedia.org/wiki/File:Squat_-_exercise_demonstration_video.webm](https://commons.wikimedia.org/wiki/File:Squat_-_exercise_demonstration_video.webm) (Creative Commons Attribution 3.0 Unported license)

Deadlift.mp4
[https://commons.wikimedia.org/wiki/File:Deadlift_-_exercise_demonstration_video.webm](https://commons.wikimedia.org/wiki/File:Deadlift_-_exercise_demonstration_video.webm) (Creative Commons Attribution 3.0 Unported license)

의 것을 사용하였다


# 향후 개선 사항
- show AR에서 panda3d의 좌표계와 Calibration을 통해 구한 현실 영상의 좌표계가 다르다. 

  좌표계들을 맞춰보려 노력하였지만, 카메라의 방향 정도만 맞췄고 위치에 대해서는 서로 차이가 있다.

  특히 카메라에서 roll이 발생할 때 좌표계의 차이가 두드러진다.

  이러한 좌표계의 차이점을 개선시켜야한다.

- 현재는 한사람의 정적인 움직임만 잘 반영되고, 여러 사람의 동적인 움직임은 잘 반영하지 못한다.
