import base64

import cv2
import numpy as np

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def read_image(stream):
    if stream is None:
        return None
    data = stream.read()
    stream.seek(0)
    if not data:
        return None
    buffer_data = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(buffer_data, cv2.IMREAD_COLOR)


def detect_faces(image):
    if image is None:
        return []
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    return [
        (int(x), int(y), int(x + w), int(y + h))
        for (x, y, w, h) in faces
    ]


def draw_faces(image, faces):
    if image is None:
        return None
    output = image.copy()
    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return output


def encode_image(image):
    if image is None:
        return ""
    ok, buffer_data = cv2.imencode(".jpg", image)
    if not ok:
        return ""
    return base64.b64encode(buffer_data.tobytes()).decode("ascii")
