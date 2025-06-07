import cv2 as cv
import numpy as np
import math
import ast

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.actor.Actor import Actor

from panda3d.core import Texture, TransparencyAttrib
from panda3d.core import LineSegs, NodePath
from panda3d.core import DirectionalLight, AmbientLight, Vec4

## === 카메라 보정 행렬 ===
# K = np.array([[645.74279809, 0, 629.74120962],
#               [0, 655.30770132, 393.42013333],
#               [0, 0, 1]])
# dist_coeff = np.array([-0.01799652, 0.19082015, -0.00970454, 0.00211079, -0.2281721])

## === 체스보드 설정 ===
# board_pattern = (10, 7)
# board_cellsize = 0.023
# obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# https://github.com/tgt5248/Visual-Copmuting/tree/main
# https://github.com/tgt5248/Visual-Copmuting/blob/main/Ar_application/panda3d.py의 코드를 참고하였다.

class AxisDemo(ShowBase):
    def __init__(
        self,
        video_path=None,
        gltf_path=None,
        animation=None,
        ShowAxis=True,
        K=None,
        dist_coeff=None,
        board_pattern=(10, 7),
        board_cellsize=0.023
    ):
        super().__init__()  
        self.ShowAxis = ShowAxis
        self.animation = animation
        self.is_paused = False  # 영상 일시정지 상태 플래그

        # === 카메라 보정 행렬 ===
        self.K = K if K is not None else np.array([[645.74279809, 0, 629.74120962],
                                                   [0, 655.30770132, 393.42013333],
                                                   [0, 0, 1]])
        self.dist_coeff = dist_coeff if dist_coeff is not None else np.array(
            [-0.01799652, 0.19082015, -0.00970454, 0.00211079, -0.2281721]
        )

        # === 체스보드 설정 ===
        self.board_pattern = board_pattern
        self.board_cellsize = board_cellsize
        self.obj_points = self.board_cellsize * np.array(
            [[c, r, 0] for r in range(self.board_pattern[1]) for c in range(self.board_pattern[0])]
        )

        # 비디오 캡처
        
        if video_path==None:
            self.cap = cv.VideoCapture(0)
        else:
            self.cap = cv.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            print("비디오를 열 수 없습니다.")
            exit()

        ret, frame = self.cap.read()
        if not ret:
            print("첫 프레임 읽기 실패")
            exit()

        h, w, _ = frame.shape
        self.w, self.h = w, h

        self.frame_w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.frame_h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # FPS 정보 추출
        self.video_fps = self.cap.get(cv.CAP_PROP_FPS)
        if self.video_fps <= 1e-2:
            self.video_fps = 30  # 웹캠인 경우 fallback
        self.frame_interval = 1.0 / self.video_fps

        # 기존 로컬 좌표계 기준 축
        self.local_axes = np.float32([
            [0.075, 0, 0],   # x축
            [0, 0.075, 0],  # y축
            [0, 0, 0.075]     # z축
        ])

        # 변환 행렬: X 그대로, Y/Z 반대
        self.flip_yz = np.array([
            [1,  0,  0],
            [0, -1,  0],
            [0,  0, -1]
        ], dtype=np.float32)

        # 변환된 축 계산
        self.flipped_axes = (self.flip_yz @ self.local_axes.T).T

        self.disableMouse()

        # === 2D 배경 설정 ===
        self.tex = Texture()
        self.tex.setup2dTexture(w, h, Texture.T_unsigned_byte, Texture.F_rgb)
        
        self.bg_img = OnscreenImage(image=self.tex, pos=(0, 0, 0))

        self.bg_img.setTransparency(TransparencyAttrib.M_none)
        self.bg_img.reparentTo(self.render2dp)
        self.bg_img.setBin("background", 0)
        self.bg_img.setDepthWrite(False)
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)

        # === 3D 캐릭터 로드 ===
        if gltf_path==None:
            self.panda = Actor("models/panda-model", {"walk": "models/panda-walk4"})
            self.panda.setScale(0.003)
            self.panda.loop("walk")
        else:
            self.panda = Actor(gltf_path)
            self.panda.setScale(0.02)
            self.panda.loop(self.animation)
        
        self.panda.setPos(0, 0, 0)
        self.panda.reparentTo(self.render)

        # === 광원 추가 ===
        # Directional Light 
        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(-45, -45, 0)
        self.render.setLight(dlnp)

        # Ambient Light
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # 축을 그리는 함수 호출
        if self.ShowAxis:
            self.draw_axes()

        # 프레임 업데이트 task
        # self.taskMgr.add(self.update_frame, "update_frame_task")
        self.taskMgr.doMethodLater(self.frame_interval, self.update_frame, "update_frame_task")

        # 초기 위치 및 스케일 저장
        self.initial_scale = self.panda.getScale()
        self.initial_pos = self.panda.getPos()

        self.key_map = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "scale_up": False,
            "scale_down": False,
            "rotate_left": False,
            "rotate_right": False,
        }

        # 키 입력 이벤트 등록
        self.accept("space", self.toggle_pause)
        self.accept("r", self.reset_transformations)
        self.accept("w", self.set_key, ["up", True])
        self.accept("w-up", self.set_key, ["up", False])
        self.accept("s", self.set_key, ["down", True])
        self.accept("s-up", self.set_key, ["down", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("q", self.set_key, ["rotate_left", True])
        self.accept("q-up", self.set_key, ["rotate_left", False])
        self.accept("e", self.set_key, ["rotate_right", True])
        self.accept("e-up", self.set_key, ["rotate_right", False])
        self.accept("p", self.set_key, ["scale_up", True])
        self.accept("p-up", self.set_key, ["scale_up", False])
        self.accept("o", self.set_key, ["scale_down", True])
        self.accept("o-up", self.set_key, ["scale_down", False])

        # 연속 입력 처리를 위한 task 추가
        self.taskMgr.add(self.handle_key_input, "handle_key_input_task")

        # print(self.K)
        # print(self.dist_coeff)
        # print(self.board_pattern)
        # print(self.board_cellsize)

    def set_key(self, key, value):
        self.key_map[key] = value

    def handle_key_input(self, task):
        speed = 0.05
        rot_speed = 1.5

        if self.key_map["up"]:
            self.move_character(0, speed, 0)
        if self.key_map["down"]:
            self.move_character(0, -speed, 0)
        if self.key_map["left"]:
            self.move_character(-speed, 0, 0)
        if self.key_map["right"]:
            self.move_character(speed, 0, 0)
        if self.key_map["rotate_left"]:
            h, p, r = self.panda.getHpr()
            self.panda.setHpr(h + rot_speed, p, r)
        if self.key_map["rotate_right"]:
            h, p, r = self.panda.getHpr()
            self.panda.setHpr(h - rot_speed, p, r)
        if self.key_map["scale_up"]:
            self.change_scale(1.01)
        if self.key_map["scale_down"]:
            self.change_scale(0.99)
        return task.cont

    def change_scale(self, factor):
        current_scale = self.panda.getScale()
        new_scale = current_scale * factor
        self.panda.setScale(new_scale)
        # print(f"Scale changed to: {new_scale}")

    def move_character(self, dx, dy, dz):
        current_pos = self.panda.getPos()
        new_pos = current_pos + (dx, dy, dz)
        self.panda.setPos(new_pos)
        # print(f"Moved to: {new_pos}")

    def reset_transformations(self):
        self.panda.setScale(self.initial_scale)
        self.panda.setPos(self.initial_pos)
        self.panda.setHpr(0, 0, 0)
        self.camera.setPos(0, 0, 0)
        self.camera.lookAt(0, 1, 0)
        # print("Transformations reset.")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        # print("Paused" if self.is_paused else "Resumed")

        if self.is_paused:
            self.saved_frame = self.panda.getCurrentFrame(self.animation)
            self.panda.pose(self.animation, self.saved_frame)

            # 이미 예약된 루프 재개 Task가 있다면 제거
            self.taskMgr.remove("resume_loop_task")

        else:
            self.panda.play(self.animation, fromFrame=self.saved_frame)

            # 중복 방지 후 예약
            self.taskMgr.remove("resume_loop_task")
            self.taskMgr.doMethodLater(
                self.get_remaining_time(), 
                self.start_loop_animation, 
                "resume_loop_task"
            )

    def start_loop_animation(self, task):
        self.panda.loop(self.animation)
        return task.done

    def get_remaining_time(self):
        anim_control = self.panda.getAnimControl(self.animation)
        total_frames = anim_control.getNumFrames()
        fps = anim_control.getPlayRate() * anim_control.getAnim().getBaseFrameRate()
        remaining_frames = total_frames - self.saved_frame
        remaining_time = remaining_frames / fps
        return remaining_time

    def draw_axes(self):
        # LineSegs 객체 생성
        lines = LineSegs()
        lines.setThickness(5.0)

        # X축 (빨강)
        lines.setColor(1, 0, 0, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(1, 0, 0)

        # Y축 (초록)
        lines.setColor(0, 1, 0, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, 1, 0)

        # Z축 (파랑)
        lines.setColor(0, 0, 1, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, 0, 1)

        # 노드로 변환하고 장면에 추가
        axis_node = lines.create()
        axis_np = NodePath(axis_node)
        # axis_np.reparentTo(self.render)
        axis_np.reparentTo(self.panda)

    def update_frame(self, task):
        if self.is_paused:
            return task.cont

        ret, frame = self.cap.read()

        # if not ret:
        #     return task.done
        if ret:
            self.last_frame = frame.copy() 
        else:
            if self.last_frame is None:
                return task.done
            frame = self.last_frame.copy()
        
        success, img_points = cv.findChessboardCorners(frame, self.board_pattern)
        if success:
            ret, rvec, tvec = cv.solvePnP(self.obj_points, img_points, self.K, self.dist_coeff)
            if self.ShowAxis:
                # 원점 위치
                origin_3d = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

                # 각 축 벡터의 끝점 계산
                axis_3d = origin_3d + self.flipped_axes

                # 카메라 투영
                axis_2d, _ = cv.projectPoints(axis_3d, rvec, tvec, self.K, self.dist_coeff)

                # OpenCV 좌표 변환 후 2D 선 그리기
                origin_2d, _ = cv.projectPoints(origin_3d, rvec, tvec, self.K, self.dist_coeff)
                origin_2d = origin_2d.reshape(-1, 2).astype(int)
                axis_2d = axis_2d.reshape(-1, 2).astype(int)

                x_end, y_end, z_end = axis_2d
                origin = origin_2d[0]

                cv.line(frame, tuple(origin), tuple(x_end), (0, 0, 255), 3)  # x축 (빨강)
                cv.line(frame, tuple(origin), tuple(y_end), (0, 255, 0), 3)  # y축 (초록)
                cv.line(frame, tuple(origin), tuple(z_end), (255, 0, 0), 3)  # z축 (파랑)

                cv.circle(frame, tuple(origin_2d[0]), radius=10, color=(0, 0, 255), thickness=3)

            R, _ = cv.Rodrigues(rvec) # Alternative) `scipy.spatial.transform.Rotation`
            p = (-R.T @ tvec).flatten()
            p_flipped = self.flip_yz @ p  # 새로운 좌표계로 변환

            view = R.T @ np.array([0, 0, 1])  # 카메라가 보는 방향
            up = R.T @ np.array([0, -1, 0])  # 카메라의 위쪽 방향

            view_flipped = self.flip_yz @ view
            up_flipped = self.flip_yz @ up        

            # 카메라 위치 텍스트 출력
            # info = f'XYZ: [{p_flipped[0]:.3f} {p_flipped[1]:.3f} {p_flipped[2]:.3f}]'
            # cv.putText(frame, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

            # 카메라 방향 텍스트 출력
            # info_view = f'ViewDir: [{view_flipped[0]:.2f}, {view_flipped[1]:.2f}, {view_flipped[2]:.2f}]'
            # cv.putText(frame, info_view, (10, 50), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

            # 카메라 up 벡터 텍스트 출력
            # info_up = f'UpVec:   [{up_flipped[0]:.2f}, {up_flipped[1]:.2f}, {up_flipped[2]:.2f}]'
            # cv.putText(frame, info_up, (10, 75), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))   

            p_flipped_100 = p_flipped * 50 # 음...

            target_x = p_flipped_100[0] + view_flipped[0]
            target_y = p_flipped_100[1] + view_flipped[1]
            target_z = p_flipped_100[2] + view_flipped[2]

            self.camera.setPos((p_flipped_100[0], p_flipped_100[1], p_flipped_100[2]))
            self.camera.lookAt((target_x, target_y, target_z), 
                               (up_flipped[0], up_flipped[1], up_flipped[2]))
            fov_x = 2 * math.atan(self.frame_w/(2 * self.K[0][0])) * 180 / math.pi
            fov_y = 2 * math.atan(self.frame_h/(2 * self.K[1][1])) * 180 / math.pi
            self.camLens.setNearFar(1, 10000)
            self.camLens.setFov(fov_x, fov_y)
            self.camLens.setAspectRatio(self.frame_w / self.frame_h)

        # OpenCV -> Panda3D 텍스처 갱신
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_rgb = np.flipud(frame_rgb)
        frame = cv.flip(frame, 0)
        self.tex.setRamImage(frame)

        # return task.cont
        return task.again if not self.is_paused else task.cont
    
def load_config_from_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    config = {}
    for line in lines:
        if '=' in line:
            key, val = line.strip().split('=', 1)
            config[key.strip()] = ast.literal_eval(val.strip())
    return config

def Show_AR(
    video_path1=None,
    gltf_path1=None,
    animation1=None,
    ShowAxis1=True,
    config_path="config.txt"
):
    config = load_config_from_txt(config_path)

    app = AxisDemo(
        video_path=video_path1,
        gltf_path=gltf_path1,
        animation=animation1,
        ShowAxis=ShowAxis1,
        K=np.array(config["K"]),
        dist_coeff=np.array(config["dist_coeff"]),
        board_pattern=tuple(config["board_pattern"]),
        board_cellsize=config["board_cellsize"]
    )
    app.run()

if __name__ == "__main__":  
    Show_AR(
        video_path1="./calv2-1.mp4",
        gltf_path1="./prototypetest1.gltf",
        animation1="dance",
        ShowAxis1=True,
        config_path="config.txt"
    )