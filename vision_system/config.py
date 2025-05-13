from pydantic_settings import BaseSettings


class CameraSettings(BaseSettings):
    """
    Configuration settings for the camera.
    """

    resolution_width: int = 3840
    resolution_height: int = 1080


class Settings(BaseSettings):
    """
    Configuration settings for the vision system.
    """

    camera_settings: CameraSettings = CameraSettings()


settings = Settings()
