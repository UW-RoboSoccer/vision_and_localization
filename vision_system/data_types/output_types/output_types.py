import sys
import pathlib

from pydantic import BaseModel

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from data_types import position_types


class TeamPosition(BaseModel):
    """
    Represents the position of a team.
    """

    bot_1_position: position_types.Position
    bot_2_position: position_types.Position
    bot_3_position: position_types.Position
    bot_4_position: position_types.Position


class LocalizationOutput(BaseModel):
    """
    Represents the output of the localization system.
    """

    us_team_position: TeamPosition
    enemy_team_position: TeamPosition
    ball_position: position_types.Position
    timestamp: float
