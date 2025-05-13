from pydantic import BaseModel


class Position(BaseModel):
    """
    Represents the position of an entity.
    Center dot is (0, 0).
    The x-axis from goal to goal, and the y-axis is from sideline to sideline.
    Our goal is negative x, enemy goal is positive x.
    Use ur brain to figure out the rest.
    Units in m.
    """

    x: float
    y: float
