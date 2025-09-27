import sys
import pathlib

import numpy as np

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from data_types.detection_types import Detection

class ObjectDistances:
    """
    Input:
        point_cloud: point cloud of the whole rectified image
        detections: list of detected blobs on the rectified image
    """
    
    @staticmethod
    def get_objects_and_distances(point_cloud: np.ndarray, detections: list[Detection]):
        """
        Get the objects and distances to them.
        """
        pass

