import sys
import pathlib
import os

import cv2
from fastapi import APIRouter, Response, WebSocket

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from providers.camera_provider import CameraProvider

router = APIRouter()

save_path = f"{str(pathlib.Path(__file__).resolve().parent.parent)}/tuning_images"


@router.post("/capture")
async def capture():
    cap = CameraProvider.get_cap()
    ret, frame = cap.read()
    if not ret:
        return {"error": "Failed to capture image"}

    shape = frame.shape
    print(f"Captured image shape: {shape}")
    left = frame[:, : shape[1] // 2]
    right = frame[:, shape[1] // 2 :]

    print(os.listdir(save_path))
    idx = (
        max([int(name.split(".")[0].split("_")[1]) for name in os.listdir(f"{save_path}/left")]) + 1
        if os.listdir(f"{save_path}/left/")
        else 0
    )
    cv2.imwrite(f"{save_path}/left/img_{idx}.jpg", left)
    cv2.imwrite(f"{save_path}/right/img_{idx}.jpg", right)
    print("Images saved successfully.")
