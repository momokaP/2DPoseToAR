import numpy as np

# 기본 관절 리스트 및 계층
joint_names = [
    "Hip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle",
    "Spine", "Thorax", "Neck", "Head",
    "LShoulder", "LElbow", "LWrist",
    "RShoulder", "RElbow", "RWrist"
]

# 관절 계층 구조
joint_hierarchy = {
    "Hip": ["RHip", "LHip", "Spine"],
    "RHip": ["RKnee"],
    "RKnee": ["RAnkle"],
    "LHip": ["LKnee"],
    "LKnee": ["LAnkle"],
    "Spine": ["Thorax"],
    "Thorax": ["Neck", "LShoulder", "RShoulder"],
    "Neck": ["Head"],
    "LShoulder": ["LElbow"],
    "LElbow": ["LWrist"],
    "RShoulder": ["RElbow"],
    "RElbow": ["RWrist"]
}

# 부모 찾기
def get_parent_map(hierarchy):
    parent_map = {}
    for parent, children in hierarchy.items():
        for child in children:
            parent_map[child] = parent
    return parent_map

parent_map = get_parent_map(joint_hierarchy)

# BVH 파일 작성 함수
def write_bvh(filename, joint_coords, frame_time=1/30):
    n_frames = joint_coords.shape[0]
    
    def offset(p, c):
        return c - p

    # 계층 출력
    def write_hierarchy(f):
        def write_joint(name, level):
            indent = "  " * level
            f.write(f"{indent}JOINT {name}\n")
            f.write(f"{indent}{{\n")
            offset_vec = joint_offsets[name]
            f.write(f"{indent}  OFFSET {offset_vec[0]:.6f} {offset_vec[1]:.6f} {offset_vec[2]:.6f}\n")
            f.write(f"{indent}  CHANNELS 3 Zrotation Xrotation Yrotation\n")
            for child in joint_hierarchy.get(name, []):
                write_joint(child, level + 1)
            if name not in joint_hierarchy:
                f.write(f"{indent}  End Site\n")
                f.write(f"{indent}  {{\n")
                f.write(f"{indent}    OFFSET 0.0 0.0 0.0\n")
                f.write(f"{indent}  }}\n")
            f.write(f"{indent}}}\n")

        # 루트
        f.write("HIERARCHY\n")
        f.write("ROOT Hip\n")
        f.write("{\n")
        root_offset = joint_offsets["Hip"]
        f.write(f"  OFFSET {root_offset[0]:.6f} {root_offset[1]:.6f} {root_offset[2]:.6f}\n")
        f.write("  CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n")
        for child in joint_hierarchy["Hip"]:
            write_joint(child, 1)
        f.write("}\n")

    # 모션 출력
    def write_motion(f):
        f.write("MOTION\n")
        f.write(f"Frames: {n_frames}\n")
        f.write(f"Frame Time: {frame_time:.6f}\n")

        for frame in joint_coords:
            motion_data = []
            # Hip: 루트 위치 + 회전
            root_pos = frame[0]
            motion_data += [f"{root_pos[0]:.6f}", f"{root_pos[1]:.6f}", f"{root_pos[2]:.6f}"]
            motion_data += ["0.0", "0.0", "0.0"]  # 단순화: 회전 없음

            # 나머지 관절들: 회전만 (회전 추정 생략, 전부 0으로)
            for name in joint_names[1:]:
                motion_data += ["0.0", "0.0", "0.0"]

            f.write(" ".join(motion_data) + "\n")

    # 오프셋 계산 (T-pose 기준: 첫 프레임 사용)
    joint_offsets = {}
    first_frame = joint_coords[0]
    for i, name in enumerate(joint_names):
        if name in parent_map:
            parent_idx = joint_names.index(parent_map[name])
            offset_vec = first_frame[i] - first_frame[parent_idx]
        else:
            offset_vec = np.array([0.0, 0.0, 0.0])  # 루트
        joint_offsets[name] = offset_vec

    # 파일 작성
    with open(filename, 'w') as f:
        write_hierarchy(f)
        write_motion(f)

# 예시 사용법
joint_coords = np.load("WalkingPutin.npy")  # (N, 17, 3)
write_bvh("WalkingPutin3.bvh", joint_coords)
