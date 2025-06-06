from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import PointLight, AmbientLight

def setup_ambient_light(node_path):
    alight = AmbientLight("alight")
    alight.setColor((0.1, 0.1, 0.1, 1))
    alnp = node_path.attachNewNode(alight)
    node_path.setLight(alnp)

def setup_point_light(node_path, pos):
    plight = PointLight("plight")
    plight.setColor((1, 1, 1, 1))
    plnp = node_path.attachNewNode(plight)
    plnp.setPos(*pos)
    node_path.setLight(plnp)
    return plnp

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.cam.setPos(0, -10, 2)
        self.cam.lookAt(0, 0, 1)

        # 모델만 렌더링
        self.model = self.loader.loadModel("TR1.gltf")
        self.model.reparentTo(self.render)

        # Armature 노드 숨기기
        armature = self.model.find("**/Armature")
        if not armature.isEmpty():
            armature.hide()
        else:
            print("⚠️ 'Armature' 노드가 발견되지 않았습니다. 노드 이름을 확인하세요.")
            self.model.ls()  # 트리 구조 확인

        setup_point_light(self.model, (5, -5, 5))
        setup_ambient_light(self.model)

game = MyGame()
game.run()