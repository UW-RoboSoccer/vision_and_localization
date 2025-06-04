import sys
import pathlib
import asyncio

import cv2
from fastapi import APIRouter, Response, WebSocket

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


@router.websocket("/ws")
async def image_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cap = CameraProvider.get_cap()

            ret, frame = cap.read()
            if not ret:
                continue

            resized_frame = cv2.resize(frame, (3840 // 4, 1080 // 4))  # Resize to 640x480 for streaming
            _, buffer = cv2.imencode(".jpg", resized_frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(1 / 15)  # 15 FPS cap
    except Exception as e:
        print("WebSocket connection closed:", e)
