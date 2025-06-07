import sys
import pathlib
import os
import json

import numpy as np
import cv2
from fastapi import APIRouter, Response, WebSocket

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from providers.camera_provider import CameraProvider

router = APIRouter()

save_prefix = f"{str(pathlib.Path(__file__).resolve().parent.parent)}/tuning_images"

chess_board_size = (7, 5)
frame_size = (3840, 1080)
square_size = 29.0


@router.post("/calibrate")
async def calibrate_camera(save_index: str | None = None):
    print(f"Calibrating camera with save index: {save_index}")
    try:
        save_path = f"{save_prefix}/saved/save_{save_index}" if save_index else save_prefix
    except:
        return {"error": "Invalid save index"}

    num_images = len(os.listdir(f"{save_path}/left"))
    if num_images == 0:
        return {"error": "No images found for calibration. Please capture images first."}

    object_points = np.zeros((chess_board_size[0] * chess_board_size[1], 3), np.float32)
    object_points[:, :2] = np.mgrid[0 : chess_board_size[0], 0 : chess_board_size[1]].T.reshape(-1, 2)
    object_points *= square_size
    object_points_list = [object_points.copy() for _ in range(num_images)]

    res_left, corner_points_left = get_corners(save_path, num_images, "left")
    res_right, corner_points_right = get_corners(save_path, num_images, "right")

    if not res_left or not res_right:
        return {"error": f"Failed to find corners in the images. res_left: {res_left}, res_right: {res_right}"}

    (
        ret_left,
        ret_right,
        ret_calibrate,
        mapx_left,
        mapy_left,
        mapx_right,
        mapy_right,
        K_left,
        D_left,
        K_right,
        D_right,
        R,
        T,
        Q,
    ) = calibrate(object_points_list, corner_points_left, corner_points_right, frame_size)

    calibration_save_path = f"{str(pathlib.Path(__file__).resolve().parent.parent)}/calibration_save"
    save_result_index = len(os.listdir(calibration_save_path))
    with open(f"{calibration_save_path}/calibration_{save_result_index}.json", "w") as f:
        json_data = {
            "ret_left": ret_left,
            "ret_right": ret_right,
            "ret_calibrate": ret_calibrate,
            "mapx_left": mapx_left.tolist(),
            "mapy_left": mapy_left.tolist(),
            "mapx_right": mapx_right.tolist(),
            "mapy_right": mapy_right.tolist(),
            "K_left": K_left.tolist(),
            "D_left": D_left.tolist(),
            "K_right": K_right.tolist(),
            "D_right": D_right.tolist(),
            "R": R.tolist(),
            "T": T.tolist(),
            "Q": Q.tolist(),
        }
        f.write(json.dumps(json_data, indent=4))

    return {
        "error": None,
        "data": {
            "ret_left": ret_left,
            "ret_right": ret_right,
            "ret_calibrate": ret_calibrate,
            "K_left": K_left.tolist(),
            "D_left": D_left.tolist(),
            "K_right": K_right.tolist(),
            "D_right": D_right.tolist(),
            "R": cv2.Rodrigues(R)[0].tolist(),
            "T": T.tolist(),
            "Q": Q.tolist(),
            "save_result_index": save_result_index,
        },
    }


def get_corners(save_path, num_images, camera_side) -> tuple[bool, list[cv2.typing.MatLike] | None]:
    corner_points = []

    for i in range(num_images):
        img_path = f"{save_path}/{camera_side}/img_{i}.jpg"
        img = cv2.imread(img_path)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(img_grey, chess_board_size, None)
        if not ret:
            print(f"Failed to find corners in {img_path}")
            return False, None
        corner_points.append(corners)

    return True, corner_points


def calibrate(object_points_list, corner_points_left, corner_points_right, frame_size):
    ret_left, K_left, D_left, rvecs_left, tvecs_left = cv2.calibrateCamera(
        object_points_list, corner_points_left, frame_size, None, None
    )
    ret_right, K_right, D_right, rvecs_right, tvecs_right = cv2.calibrateCamera(
        object_points_list, corner_points_right, frame_size, None, None
    )
    print(f"Left camera calibration: {ret_left}, Right camera calibration: {ret_right}")

    ret_calibrate, K_left, D_left, K_right, D_right, R, T, E, F = cv2.stereoCalibrate(
        object_points_list,
        corner_points_left,
        corner_points_right,
        K_left,
        D_left,
        K_right,
        D_right,
        frame_size,
        None,
        None,
        None,
        None,
    )
    print(f"Stereo calibration: {ret_calibrate}")

    R_left, R_right, P_left, P_right, Q, roi1, roi2 = cv2.stereoRectify(
        K_left, D_left, K_right, D_right, frame_size, R, T
    )

    mapx_left, mapy_left = cv2.initUndistortRectifyMap(K_left, D_left, R_left, P_left, frame_size, cv2.CV_32FC1)
    mapx_right, mapy_right = cv2.initUndistortRectifyMap(K_right, D_right, R_right, P_right, frame_size, cv2.CV_32FC1)

    return (
        ret_left,
        ret_right,
        ret_calibrate,
        mapx_left,
        mapy_left,
        mapx_right,
        mapy_right,
        K_left,
        D_left,
        K_right,
        D_right,
        R,
        T,
        Q,
    )
