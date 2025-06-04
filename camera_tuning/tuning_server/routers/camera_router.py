import sys
import pathlib

import cv2
from fastapi import APIRouter, Response

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from providers.camera_provider import CameraProvider

router = APIRouter()


@router.get("/image")
async def get_image():
    cap = CameraProvider.get_cap()
    ret, frame = cap.read()
    if not ret:
        return {"error": "Failed to capture image"}

    ret, encoded_image = cv2.imencode(".jpg", frame)
    if not ret:
        return {"error": "Failed to encode image"}

    return Response(content=encoded_image.tobytes(), media_type="image/jpg")
