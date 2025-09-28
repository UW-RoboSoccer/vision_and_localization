import sys
import pathlib
import asyncio

import cv2
from fastapi import APIRouter, WebSocket
import numpy as np

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from providers.calibration_provider import CalibrationProvider
from providers.camera_provider import CameraProvider

router = APIRouter()

calibration_save_path = f"{str(pathlib.Path(__file__).resolve().parent.parent)}/calibration_save"

frame_size = (3840, 1080)
stereo = cv2.StereoSGBM.create(
    minDisparity=0,
    numDisparities=128,
    blockSize=9,
    P1=8 * 3 * 9**2,
    P2=32 * 3 * 9**2,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    disp12MaxDiff=1,
)


@router.post("/load_calibration")
async def load_calibration(save_index: str) -> dict[str, bool]:
    calibration_set = CalibrationProvider.set_calibration(save_index)
    return {"success": calibration_set}


def measure_distance(stereo_frame, stereo, mapx_left, mapy_left, mapx_right, mapy_right):
    grey_frame = cv2.cvtColor(stereo_frame, cv2.COLOR_BGR2GRAY)

    grey_frame_left = grey_frame[:, : frame_size[0] // 2]
    grey_frame_right = grey_frame[:, frame_size[0] // 2 :]

    remap_left = cv2.remap(grey_frame_left, mapx_left, mapy_left, cv2.INTER_LINEAR)
    remap_right = cv2.remap(grey_frame_right, mapx_right, mapy_right, cv2.INTER_LINEAR)

    disparity = stereo.compute(np.uint8(remap_left), np.uint8(remap_right)).astype(np.float32) / 16.0

    return disparity


def get_point_cloud(disparity, Q):
    point_cloud = cv2.reprojectImageTo3D(disparity, Q)
    depth = point_cloud[:, :, 2]

    depth_vis = np.clip(depth, 300, 1500)  # Adjust these bounds as needed
    depth_vis = cv2.normalize(depth_vis, None, 0, 255, cv2.NORM_MINMAX)
    depth_vis = np.uint8(depth_vis)
    depth_colored = cv2.applyColorMap(depth_vis, cv2.COLORMAP_PLASMA)
    return depth_colored


@router.websocket("/ws")
async def distance_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            calibration = CalibrationProvider.get_calibration()
            if not calibration:
                await asyncio.sleep(1)
                continue

            mapx_left = np.array(calibration["mapx_left"], dtype=np.float32)
            mapy_left = np.array(calibration["mapy_left"], dtype=np.float32)
            mapx_right = np.array(calibration["mapx_right"], dtype=np.float32)
            mapy_right = np.array(calibration["mapy_right"], dtype=np.float32)
            Q = np.array(calibration["Q"], dtype=np.float64)

            cap = CameraProvider.get_cap()
            ret, frame = cap.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue

            disparity = measure_distance(frame, stereo, mapx_left, mapy_left, mapx_right, mapy_right)
            point_cloud = get_point_cloud(disparity, Q)

            _, buffer = cv2.imencode(".jpg", point_cloud)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(1)  # 15 FPS cap
    except Exception as e:
        print("WebSocket connection closed:", e)
