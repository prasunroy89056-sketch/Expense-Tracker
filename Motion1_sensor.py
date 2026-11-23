import cv2
import os
import time
from datetime import datetime

# Create folder for motion images
folder = "motion_images"

if not os.path.exists(folder):
    os.makedirs(folder)

# Start camera
camera = cv2.VideoCapture(0)

# Camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Read first frame
ret, previous = camera.read()

if not ret:
    print("Camera could not be opened!")
    exit()

previous = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
previous = cv2.GaussianBlur(previous, (21, 21), 0)

motion_count = 0
motion_start = None
last_saved = 0

print("Smart Motion Detector Started")
print("Press Q to exit")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur image to reduce noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Find difference between frames
    difference = cv2.absdiff(previous, gray)

    # Threshold
    _, threshold = cv2.threshold(
        difference,
        25,
        255,
        cv2.THRESH_BINARY
    )

    # Remove small noise
    threshold = cv2.dilate(threshold, None, iterations=2)

    # Find moving objects
    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion_detected = False

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore very small movements
        if area < 1000:
            continue

        motion_detected = True

        # Get object position
        x, y, w, h = cv2.boundingRect(contour)

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

    # Motion detected
    if motion_detected:

        if motion_start is None:
            motion_start = time.time()
            motion_count += 1

        duration = time.time() - motion_start

        status = "MOTION DETECTED"

        # Save image every 3 seconds
        if time.time() - last_saved > 3:

            filename = datetime.now().strftime(
                "%Y%m%d_%H%M%S.jpg"
            )

            filepath = os.path.join(
                folder,
                filename
            )

            cv2.imwrite(filepath, frame)

            last_saved = time.time()

            print("Motion image saved:", filepath)

    else:

        motion_start = None
        duration = 0

        status = "NO MOTION"

    # Current time
    current_time = datetime.now().strftime(
        "%d-%m-%Y  %H:%M:%S"
    )

    # Status background
    cv2.rectangle(
        frame,
        (0, 0),
        (500, 145),
        (30, 30, 30),
        -1
    )

    # Project title
    cv2.putText(
        frame,
        "SMART MOTION DETECTOR",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Status
    cv2.putText(
        frame,
        "STATUS: " + status,
        (15, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255) if motion_detected else (0, 255, 0),
        2
    )

    # Motion count
    cv2.putText(
        frame,
        "Motion Count: " + str(motion_count),
        (15, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Motion duration
    cv2.putText(
        frame,
        "Duration: " + str(round(duration, 1)) + " sec",
        (15, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Time
    cv2.putText(
        frame,
        current_time,
        (15, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    # Show camera
    cv2.imshow(
        "Smart Motion Detector",
        frame
    )

    # Update previous frame
    previous = gray

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera
camera.release()

# Close all windows
cv2.destroyAllWindows()

print("Motion Detector stopped.")
