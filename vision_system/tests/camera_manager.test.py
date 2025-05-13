import sys
import pathlib

import cv2

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from input_managers import camera_manager

camera_manager = camera_manager.CameraManager(0)

_, img = camera_manager.capture_image()
print(f"Left image shape: {img.left_image.shape}")
print(f"Right image shape: {img.right_image.shape}")
print(f"Timestamp: {img.timestamp}")

cv2.imwrite("tests/images/left_image.jpg", img.left_image)
cv2.imwrite("tests/images/right_image.jpg", img.right_image)
print("Images saved as left_image.jpg and right_image.jpg")
