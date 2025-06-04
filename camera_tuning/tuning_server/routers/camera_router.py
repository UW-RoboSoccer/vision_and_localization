import sys
import pathlib
import asyncio

import cv2
from fastapi import APIRouter, Response, WebSocket

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from providers.camera_provider import CameraProvider

router = APIRouter()


def calculate_blurriness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var


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
            left = frame[:, : frame.shape[1] // 2, :]
            right = frame[:, frame.shape[1] // 2 :, :]
            left_blurriness = calculate_blurriness(left)
            right_blurriness = calculate_blurriness(right)
            cv2.putText(
                resized_frame,
                f"Left Blurriness: {left_blurriness:.2f}, Right Blurriness: {right_blurriness:.2f}",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
            _, buffer = cv2.imencode(".jpg", resized_frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(1 / 15)  # 15 FPS cap
    except Exception as e:
        print("WebSocket connection closed:", e)
