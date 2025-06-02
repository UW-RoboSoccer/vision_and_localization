import cv2
import time

print("Testing video stream capture...")
frame_size = (3840, 1080)

cap = cv2.VideoCapture(1)
print("Video capture opened")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size[1])
print("Video capture properties set")


def calculate_blurriness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var


while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    print(f"Frame captured {frame.shape}")
    resized = cv2.resize(frame, (1920, 540))

    left = frame[:, : frame.shape[1] // 2, :]
    right = frame[:, frame.shape[1] // 2 :, :]
    left_blurriness = calculate_blurriness(left)
    right_blurriness = calculate_blurriness(right)
    cv2.putText(
        resized,
        f"Left Blurriness: {left_blurriness:.2f}, Right Blurriness: {right_blurriness:.2f}",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

    cv2.imshow("Frame", resized)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
