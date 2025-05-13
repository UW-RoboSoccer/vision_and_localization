import cv2
from pydantic import BaseModel


class ImageCapture(BaseModel):
    """
    Represents an image captured by a camera.
    """

    left_image: cv2.typing.MatLike
    right_image: cv2.typing.MatLike
    timestamp: float
