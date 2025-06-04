import sys
import pathlib
import os
import shutil

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

    os.makedirs(f"{save_path}/left", exist_ok=True)
    os.makedirs(f"{save_path}/right", exist_ok=True)

    idx = len(os.listdir(f"{save_path}/left"))
    cv2.imwrite(f"{save_path}/left/img_{idx}.jpg", left)
    cv2.imwrite(f"{save_path}/right/img_{idx}.jpg", right)
    print("Images saved successfully.")
