import cv2 as cv
import numpy as np
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import Texture, TransparencyAttrib
from direct.actor.Actor import Actor
from panda3d.core import Point3
from panda3d.core import Mat4, LMatrix4f
import panda3d.core as p3c
from panda3d.core import LineSegs, NodePath
from scipy.spatial.transform import Rotation as Rscipy
import math
from panda3d.core import DirectionalLight, AmbientLight, Vec4
from panda3d.core import Vec3, Point3
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

# === 카메라 보정 행렬 ===
K = np.array([[645.74279809, 0, 629.74120962],
              [0, 655.30770132, 393.42013333],
              [0, 0, 1]])
dist_coeff = np.array([-0.01799652, 0.19082015, -0.00970454, 0.00211079, -0.2281721])

# === 체스보드 설정 ===
board_pattern = (10, 7)
board_cellsize = 0.023
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# square_size = 40
square_size = board_cellsize

class AxisDemo(ShowBase):
    def __init__(self):
        super().__init__()  
        self.is_paused = False  # 영상 일시정지 상태 플래그
        self.accept("space", self.toggle_pause)  # 스페이스바 누르면 토글

        # 비디오 캡처
        self.cap = cv.VideoCapture('./calv2-1.mp4')
        # self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("비디오를 열 수 없습니다.")
            exit()

        ret, frame = self.cap.read()
        if not ret:
            print("첫 프레임 읽기 실패")
            exit()

        h, w, _ = frame.shape
        self.w, self.h = w, h

        # 카메라 위치 조정
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
        # self.panda = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.panda = Actor("./2d3dartest1.gltf")
        self.panda.reparentTo(self.render)
        # self.panda.setScale(0.002)
        self.panda.setScale(0.1)
        self.panda.setPos(0, 0, 0)  # 카메라 앞으로
        # self.panda.loop("walk")
        self.panda.loop("dance1")
        
        # self.panda2 = Actor("models/panda",{"walk": "models/panda-walk"})
        # self.panda2.reparentTo(self.render)
        # self.panda2.setScale(0.1)
        # self.panda2.setPos(0, 0, 0)  # 카메라 앞으로
        # self.panda2.loop("walk")

        # === 광원 추가 ===

        # Directional Light (태양광 느낌)
        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(-45, -45, 0)  # 광원 방향 설정
        self.render.setLight(dlnp)

        # Ambient Light (전체 조명)
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # 축을 그리는 함수 호출
        self.draw_axes()

        self.camera.setPos(5, -15, 7)
        self.camera.lookAt(0, 0, 0)

        # 프레임 업데이트 task
        self.taskMgr.add(self.update_frame, "update_frame_task")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        print("Paused" if self.is_paused else "Resumed")

    def draw_axes(self):
        # LineSegs 객체 생성
        lines = LineSegs()
        lines.setThickness(5.0)

        # X축 (빨강)
        lines.setColor(1, 0, 0, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(3, 0, 0)

        # Y축 (초록)
        lines.setColor(0, 1, 0, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, 3, 0)

        # Z축 (파랑)
        lines.setColor(0, 0, 1, 1)
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, 0, 3)

        # 노드로 변환하고 장면에 추가
        axis_node = lines.create()
        axis_np = NodePath(axis_node)
        axis_np.reparentTo(self.render)

    def update_frame(self, task):
        if self.is_paused:
            return task.cont

        ret, frame = self.cap.read()
        if not ret:
            return task.done
        
        success, img_points = cv.findChessboardCorners(frame, board_pattern)
        if success:
            frame_w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
            frame_h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

            ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

            # 기존 로컬 좌표계 기준 축
            local_axes = np.float32([
                [0.05, 0, 0],   # x축
                [0, 0.075, 0],  # y축
                [0, 0, 0.1]     # z축
            ])

            # 변환 행렬: X 그대로, Y/Z 반대
            flip_yz = np.array([
                [1,  0,  0],
                [0, -1,  0],
                [0,  0, -1]
            ], dtype=np.float32)

            # 변환된 축 계산
            flipped_axes = (flip_yz @ local_axes.T).T

            # 원점 위치
            origin_3d = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

            # 각 축 벡터의 끝점 계산
            axis_3d = origin_3d + flipped_axes

            # 카메라 투영
            axis_2d, _ = cv.projectPoints(axis_3d, rvec, tvec, K, dist_coeff)

            # OpenCV 좌표 변환 후 2D 선 그리기
            origin_2d, _ = cv.projectPoints(origin_3d, rvec, tvec, K, dist_coeff)
            origin_2d = origin_2d.reshape(-1, 2).astype(int)
            axis_2d = axis_2d.reshape(-1, 2).astype(int)

            x_end, y_end, z_end = axis_2d
            origin = origin_2d[0]

            cv.line(frame, tuple(origin), tuple(x_end), (0, 0, 255), 3)  # x축 (빨강)
            cv.line(frame, tuple(origin), tuple(y_end), (0, 255, 0), 3)  # y축 (초록)
            cv.line(frame, tuple(origin), tuple(z_end), (255, 0, 0), 3)  # z축 (파랑)

            # 원 그리기
            cv.circle(frame, tuple(origin_2d[0]), radius=10, color=(0, 0, 255), thickness=3)

            R, _ = cv.Rodrigues(rvec) # Alternative) `scipy.spatial.transform.Rotation`
            p = (-R.T @ tvec).flatten()
            p_flipped = flip_yz @ p  # 새로운 좌표계로 변환

            info = f'XYZ: [{p_flipped[0]:.3f} {p_flipped[1]:.3f} {p_flipped[2]:.3f}]'
            cv.putText(frame, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

            view = R.T @ np.array([0, 0, 1])  # 카메라가 보는 방향
            up = R.T @ np.array([0, -1, 0])  # 카메라의 위쪽 방향

            view_flipped = flip_yz @ view
            up_flipped = flip_yz @ up        

            # 카메라 방향 텍스트 출력
            info_view = f'ViewDir: [{view_flipped[0]:.2f}, {view_flipped[1]:.2f}, {view_flipped[2]:.2f}]'
            cv.putText(frame, info_view, (10, 50), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

            # 카메라 up 벡터 텍스트 출력
            info_up = f'UpVec:   [{up_flipped[0]:.2f}, {up_flipped[1]:.2f}, {up_flipped[2]:.2f}]'
            cv.putText(frame, info_up, (10, 75), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))   

            p_flipped_100 = p_flipped * 50

            target_x = p_flipped_100[0] + view_flipped[0]
            target_y = p_flipped_100[1] + view_flipped[1]
            target_z = p_flipped_100[2] + view_flipped[2]

            self.camera.setPos((p_flipped_100[0], p_flipped_100[1], p_flipped_100[2]))
            self.camera.lookAt((target_x, target_y, target_z), 
                               (up_flipped[0], up_flipped[1], up_flipped[2]))

            fov_x = 2 * math.atan(frame_w/(2 * K[0][0])) * 180 / math.pi
            fov_y = 2 * math.atan(frame_h/(2 * K[1][1])) * 180 / math.pi
            self.camLens.setNearFar(1, 10000)
            self.camLens.setFov(fov_x, fov_y)
            self.camLens.setAspectRatio(frame_w / frame_h)

        # OpenCV -> Panda3D 텍스처 갱신
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_rgb = np.flipud(frame_rgb)
        #self.tex.set_ram_image(frame_rgb.tobytes())
        frame = cv.flip(frame, 0)
        self.tex.setRamImage(frame)

        return task.cont

if __name__ == "__main__":
    app = AxisDemo()
    app.run()
