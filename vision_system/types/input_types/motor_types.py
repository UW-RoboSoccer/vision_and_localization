from pydantic import BaseModel


class MotorPosition(BaseModel):
    """
    Represents the position of the camera's motors.
    TODO: ask mech and fw to confirm
    """

    position: float
    timestamp: float
