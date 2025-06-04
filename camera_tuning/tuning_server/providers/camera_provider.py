import cv2


class CameraProvider:
    cap = None

    @classmethod
    def get_cap(cls, camera_index: int = 0):
        if cls.cap:
            if cls.cap.isOpened():
                print("Camera already opened")
                return cls.cap
            else:
                print("Camera not opened, reinitializing")
            return cls.cap

        print("getting camera", camera_index)
        cls.cap = cv2.VideoCapture(camera_index)
        print("Camera initialized:", cls.cap.isOpened())

        cls.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        cls.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        return cls.cap

    def capture_image(self) -> tuple[bool, tuple[cv2.typing.MatLike, cv2.typing.MatLike] | None]:
        ret, frame = self.cap.read()
        if not ret:
            return False, None

        shape = frame.shape

        left_image = frame[:, : shape[1] // 2, :]
        right_image = frame[:, shape[1] // 2 :, :]

        return True, left_image, right_image


cap = CameraProvider.get_cap(0)
