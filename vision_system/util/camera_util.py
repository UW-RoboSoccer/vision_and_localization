def list_connected_cameras():
    """
    List all connected cameras and their indices.
    """
    import cv2

    camera_indices = []
    for i in range(10):  # Check the first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:  # Check if the camera is opened successfully
            print(f"Camera found at index {i}")
            camera_indices.append(i)
        cap.release()

    return camera_indices
