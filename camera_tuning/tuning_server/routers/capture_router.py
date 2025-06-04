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


@router.post("/clear")
async def clear_images():
    left_path = f"{save_path}/left"
    right_path = f"{save_path}/right"

    for filename in os.listdir(left_path):
        file_path = os.path.join(left_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for filename in os.listdir(right_path):
        file_path = os.path.join(right_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return {"message": "Images cleared successfully."}


@router.post("/save")
async def save_images():
    os.makedirs(f"{save_path}/saved", exist_ok=True)
    save_folder = f"{save_path}/saved/save_{len(os.listdir(f'{save_path}/saved'))}"
    print(f"Saving images to {save_folder}")
    os.makedirs(save_folder, exist_ok=True)
    shutil.copytree(f"{save_path}/left", f"{save_folder}/left")
    shutil.copytree(f"{save_path}/right", f"{save_folder}/right")

    return {"message": "Images saved successfully."}
