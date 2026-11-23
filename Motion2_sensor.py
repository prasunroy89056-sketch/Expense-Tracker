import cv2

camera = cv2.VideoCapture(0)

ret, previous = camera.read()

previous = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
previous = cv2.GaussianBlur(previous, (21, 21), 0)

while True:
    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    difference = cv2.absdiff(previous, gray)

    _, threshold = cv2.threshold(
        difference, 25, 255, cv2.THRESH_BINARY
    )

    motion = cv2.countNonZero(threshold)

    if motion > 5000:
        cv2.putText(
            frame,
            "Motion Detected!",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
    else:
        cv2.putText(
            frame,
            "No Motion",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Motion Sensor", frame)

    previous = gray

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

