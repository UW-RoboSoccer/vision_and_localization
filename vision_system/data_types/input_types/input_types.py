import sys
import pathlib

from pydantic import BaseModel

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from data_types.input_types import camera_types, motor_types


class InputData(BaseModel):
    """
    Represents the input data for the vision system.
    """

    image_capture: camera_types.ImageCapture
    motor_position: motor_types.MotorPosition
    timestamp: float
