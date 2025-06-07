import numpy as np
from scipy.spatial.transform import Rotation as R

joint_names = [
    "Hips", "RHip", "RKnee", "RFoot", "LHip", "LKnee", "LFoot",
    "Spine", "Thorax", "Neck", "Head", "LShoulder", "LElbow", "LWrist",
    "RShoulder", "RElbow", "RWrist"
]
parent = [-1, 0, 1, 2, 0, 4, 5, 0, 7, 8, 9, 8, 11, 12, 8, 14, 15]

def compute_offsets(joint_positions):
    return [joint_positions[i] - joint_positions[parent[i]] if parent[i] != -1 else joint_positions[i]
            for i in range(len(joint_names))]

def rotation_between(v1, v2):
    axis = np.cross(v1, v2)
    if np.linalg.norm(axis) < 1e-5:
        return np.zeros(3)
    angle = np.arccos(np.clip(np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6), -1.0, 1.0))
    rotvec = axis / np.linalg.norm(axis) * angle
    return R.from_rotvec(rotvec).as_euler('zxy', degrees=True)

def write_bvh(joint_positions, output_path, frame_time=1/50):
    N = joint_positions.shape[0]
    offsets = compute_offsets(joint_positions[0])

    with open(output_path, 'w') as f:
        # Header
        def write_joint(idx, indent):
            pad = '\t' * indent
            name = joint_names[idx]
            f.write(f"{pad}JOINT {name}\n")
            f.write(f"{pad}{{\n")
            offset = offsets[idx]
            f.write(f"{pad}\tOFFSET {offset[0]:.6f} {offset[1]:.6f} {offset[2]:.6f}\n")
            f.write(f"{pad}\tCHANNELS 3 Zrotation Xrotation Yrotation\n")
            for child in [i for i, p in enumerate(parent) if p == idx]:
                write_joint(child, indent + 1)
            if not any(p == idx for p in parent):
                f.write(f"{pad}\tEnd Site\n{pad}\t{{\n{pad}\t\tOFFSET 0 0 0\n{pad}\t}}\n")
            f.write(f"{pad}}}\n")

        f.write("HIERARCHY\nROOT Hips\n{\n")
        offset = offsets[0]
        f.write(f"\tOFFSET {offset[0]:.6f} {offset[1]:.6f} {offset[2]:.6f}\n")
        f.write("\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n")
        for child in [i for i, p in enumerate(parent) if p == 0]:
            write_joint(child, 1)
        f.write("}\n")

        # Motion
        f.write("MOTION\n")
        f.write(f"Frames: {N}\n")
        f.write(f"Frame Time: {frame_time:.6f}\n")

        for t in range(N):
            frame = joint_positions[t]
            root_pos = frame[0]
            motion_line = [f"{root_pos[0]:.6f}", f"{root_pos[1]:.6f}", f"{root_pos[2]:.6f}"]

            for i in range(len(joint_names)):
                if parent[i] == -1:
                    # 루트 회전 (예: RHip - Hips 사용)
                    prev_vec = joint_positions[0][1] - joint_positions[0][0]
                    cur_vec = frame[1] - frame[0]
                else:
                    prev_vec = joint_positions[0][i] - joint_positions[0][parent[i]]
                    cur_vec = frame[i] - frame[parent[i]]

                euler = rotation_between(prev_vec, cur_vec)
                motion_line += [f"{angle:.6f}" for angle in euler]

            f.write(" ".join(motion_line) + "\n")

# 사용 예
keypoints3d = np.load("dance2.npy")  # (N, 17, 3)
write_bvh(keypoints3d, "dance2test8.bvh")
