import os
from bvh_skeleton import h36m_skeleton
import numpy as np

# 将3dpoint转换为标准的bvh格式并输出到outputs/outputvideo/alpha_pose_视频名/bvh下
def write_standard_bvh(outbvhfilepath,prediction3dpoint):
    '''
    :param outbvhfilepath: 输出bvh动作文件路径
    :param prediction3dpoint: 预测的三维关节点
    :return:
    '''

    # 将预测的点放大100倍
    for frame in prediction3dpoint:
        for point3d in frame:
            point3d[0] *= 100
            point3d[1] *= 100
            point3d[2] *= 100

            # 交换Y和Z的坐标
            #X = point3d[0]
            #Y = point3d[1]
            #Z = point3d[2]

            #point3d[0] = -X
            #point3d[1] = Z
            #point3d[2] = Y

    dir_name = os.path.dirname(outbvhfilepath)
    basename = os.path.basename(outbvhfilepath)
    video_name = basename[:basename.rfind('.')]
    bvhfileDirectory = os.path.join(dir_name,video_name,"bvh")
    if not os.path.exists(bvhfileDirectory):
        os.makedirs(bvhfileDirectory)
    bvhfileName = os.path.join(dir_name,video_name,"bvh","{}.bvh".format(video_name))
    human36m_skeleton = h36m_skeleton.H36mSkeleton()
    human36m_skeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)

# 예: 10프레임, 17관절, (x, y, z) 좌표
prediction3dpoint = np.load("dance2.npy")

# 출력될 bvh 경로 지정
out_path = "dance2"

# BVH 파일 생성
write_standard_bvh(out_path, prediction3dpoint)