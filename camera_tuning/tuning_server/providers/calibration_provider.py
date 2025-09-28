import os
import pathlib
import json

calibration_save_path = f"{str(pathlib.Path(__file__).resolve().parent.parent)}/calibration_save"


class CalibrationProvider:
    calibration = None

    @classmethod
    def set_calibration(cls, calibration_index: str) -> bool:
        if not calibration_index:
            return False

        calibration_file_path = f"{calibration_save_path}/calibration_{calibration_index}.json"
        if not os.path.exists(calibration_file_path):
            return False

        with open(calibration_file_path, "r") as f:
            cls.calibration = json.load(f)
        return True

    @classmethod
    def get_calibration(cls):
        return cls.calibration
