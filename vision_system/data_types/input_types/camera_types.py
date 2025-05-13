import cv2
from pydantic import BaseModel, ConfigDict


class ImageCapture(BaseModel):
    """
    Represents an image captured by a camera.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    left_image: cv2.typing.MatLike
    right_image: cv2.typing.MatLike
    timestamp: float
