import numpy as np
import cv2 as cv
import os

def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    img_select = []
    while True:
        valid, img = video.read()
        if not valid:
            break
        if select_all:
            img_select.append(img)
        else:
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10,25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0,255,0))
            cv.imshow(wnd_name, display)

            key = cv.waitKey(wait_msec)
            if key == ord(' '):
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)
            if key == 27:
                break
    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    obj_pts = [[c,r,0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)

    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)

def run_camera_calibration(video_file, board_pattern, board_cellsize):
    # 비디오 파일 이름에서 확장자를 제거하고 저장 파일 이름 생성
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    output_file = f'{base_name}_calibration_result.txt'

    img_select = select_img_from_video(video_file, board_pattern)
    if len(img_select) <= 0:
        print('There is no selected images!')
        return 

    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    camera_matrix_list = K.tolist()
    camera_matrix_str = "[" + ", ".join(
        "[" + ", ".join(f"{val:.8f}" for val in row) + "]"
        for row in camera_matrix_list
    ) + "]"

    result_str = (
        '## Camera Calibration Results\n'
        f'* The number of selected images = {len(img_select)}\n'
        f'* RMS error = {rms:.6f}\n'
        f'* Camera matrix (K) = {camera_matrix_str}\n'
        f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten().tolist()}\n'
        f'* board_pattern = ({board_pattern[0]}, {board_pattern[1]})\n'
        f'* board_cellsize = {board_cellsize}\n'
    )

    # print(result_str)

    with open(output_file, 'w') as f:
        f.write(result_str)

    print(f'Results saved to: {output_file}')

    return output_file

if __name__ == '__main__':
    video_file = './KakaoTalk_20250405_210903239.mp4'
    board_pattern = (10, 7)
    board_cellsize = 0.023
    run_camera_calibration(video_file, board_pattern, board_cellsize)