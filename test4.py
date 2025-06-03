import os
import sys

# 현재 파일 기준으로 VideoPose3D/data 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'VideoPose3D', 'data')
if data_dir not in sys.path:
    sys.path.insert(0, data_dir)

# 이제 import 가능
from prepare_data_2d_custom import decode
from prepare_data_2d_custom import output_prefix_2d
from data_utils import suggest_metadata

print(output_prefix_2d)
