import sys
import pathlib
import datetime

import cv2

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from config import settings
from data_types.input_types import camera_types


class CameraManager:
    """
    A class to manage camera input for the vision system.
    It handles the initialization, configuration, and capture of images from the camera.
    """

    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.camera_settings.resolution_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.camera_settings.resolution_height)

    def capture_image(self) -> tuple[bool, camera_types.ImageCapture | None]:
        """
        Captures an image from the camera.
        Returns an ImageCapture object containing the captured image.
        """
        ret, frame = self.cap.read()
        if not ret:
            return False, None

        shape = frame.shape

        left_image = frame[:, : shape[1] // 2, :]
        right_image = frame[:, shape[1] // 2 :, :]

        return True, camera_types.ImageCapture(
            left_image=left_image, right_image=right_image, timestamp=datetime.datetime.now().timestamp()
        )
