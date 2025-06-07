# 이 프로젝트에서의 blender 사용 방법

- .bvh 파일 편집 프로그램으로 blender가 필요하다.
- [blender 2.83](https://www.blender.org/download/releases/2-83/) 버전을 사용하였다.
  
  (최신 버전의 blender는 .bvh 애니메이션이 적용된 캐릭터를 panda3d에서 불러올 때 문제가 생긴다.)


## .bvh 적용  
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

- (5) 애니메이션 관절을 선택하고 블랜더 화면 오른쪽 아래의 사람 모양의 아이콘(object data properties)을 클릭한 뒤, Rest Position을 클릭하여 미리 설정해 놓은 캐릭터와 같은 자세가 되도록 한다. 이후 캐릭터와 애니메이션 관절을 모두 선택하고, ctrl + p를 누른 뒤, Armature Deform의 With Automatic Weights를 클릭한다.
![307](https://github.com/user-attachments/assets/a64bb26c-0e72-421b-95bf-0319d8553888)
![308](https://github.com/user-attachments/assets/4f6d81b6-91e8-4fc1-9b4e-3c731b2c5f75)

- (6) .bvh의 애니메이션과 캐릭터가 잘 연결되면 Pose를 선택하고 블랜더 화면 오른쪽의 사람 모양의 아이콘(object data properties)을 클릭한 뒤, Pose Position을 클릭하고 애니메이션을 재생하여 움직임을 관찰한다.
![309](https://github.com/user-attachments/assets/1056aa3a-d3aa-4720-ab36-ae2afbb36a05)

- (7) 애니메이션의 이름을 지정한다. show_ar을 사용할 때 이 애니메이션 이름을 입력해야 한다. 여기서는 animation으로 하였다.
![333](https://github.com/user-attachments/assets/8954e451-9603-415b-924a-c8338d82316b)

- (8) 블랜더 화면 오른쪽 아래의 노란 사각형 모양의 아이콘(object properties)를 클릭하면 캐릭터의 위치, 회전, 크기를 조절할 수 있다.

  convert_video_to_bvh에서 만든 .bvh파일은 애니메이션 관절이 반대로 뒤집혀져 있으므로, y축 기준으로 180도 회전시킨다.

![310](https://github.com/user-attachments/assets/27b940d3-da36-41f3-ac9e-099ba76b7f34)
![311](https://github.com/user-attachments/assets/992afe59-1ac3-447a-ab47-34ef6533b636)


## blender에서 .gltf 파일 export
- show_ar에서 사용할 애니메이션 캐릭터를 만들기 위해 애니메이션이 적용된 캐릭터를 .gltf 파일로 export 해야한다.
- (1) blender 화면 위의 file->export->glTF 클릭

![312](https://github.com/user-attachments/assets/bdd7dbc3-9ef6-4a42-8ab8-cb268ff818dc)

- (2) Format을 glTF Entedded(.gltf)로 설정하고 Export glTF 2.0 버튼 클릭

![313](https://github.com/user-attachments/assets/e9e1d54e-02a5-4697-9aa3-db092bae1888)

- (3) 확인

![314](https://github.com/user-attachments/assets/6717a543-28c5-4f2d-8c61-4ffb73b0c04b)
![315](https://github.com/user-attachments/assets/372451dc-cfa6-474f-812d-6b8c6ada2a27)
![316](https://github.com/user-attachments/assets/28b566a1-db03-4070-9386-ef692295acff)
