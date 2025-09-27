from pydantic import BaseModel

class Detection(BaseModel):
    """
    Represents a detection of an object.
    """

    x: float
    y: float
    w: float
    h: float
