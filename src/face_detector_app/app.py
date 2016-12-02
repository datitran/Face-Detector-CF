import os
import cv2
import numpy as np
from PIL import Image
from StringIO import StringIO
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))


def detect_faces(image):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = Image.open(StringIO(image))
    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_RGBA2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    try:
        return faces.tolist()
    except:
        return []


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def prediction():
    """
    curl -X POST -v -H "Content-Type: image/png" --data-binary @abba.png http://127.0.0.1:9099/prediction -o foo.jpg
    """
    if request.method == "POST":
        image = request.data
        face_coordinates = detect_faces(image)
        return jsonify(faces=face_coordinates)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
