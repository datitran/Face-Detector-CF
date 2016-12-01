import os
import base64
import cv2
import numpy as np
from flask import Flask, request
from flask_cors import CORS, cross_origin
from PIL import Image

app = Flask(__name__)
cors = CORS(app)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))


def detect_faces(image):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = Image.open(image)
    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img_cv2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return base64.b64encode(img_cv2)


@app.route("/")
def main():
    return "Hello World!"


@app.route("/prediction", methods=["POST"])
def prediction():
    """
    curl -i -X POST -F files=@abba.png http://0.0.0.0:9099/prediction
    """
    if request.method == "POST":
        image = request.files["files"]
        image_faces = detect_faces(image)
        return str(image_faces)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
