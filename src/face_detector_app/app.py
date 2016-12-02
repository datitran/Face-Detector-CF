import os
import cv2
from StringIO import StringIO
import numpy as np
from flask import Flask, request, make_response, render_template
from flask_cors import CORS, cross_origin
from PIL import Image

app = Flask(__name__)
cors = CORS(app)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))


def detect_faces(image):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = Image.open(StringIO(image))
    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA)
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

    img_pil = Image.fromarray(img_cv2)
    buffer = StringIO()
    img_pil.save(buffer, format="JPEG")

    return buffer.getvalue()


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
        image_faces = detect_faces(image)
        response = make_response(image_faces)
        response.headers["Content-Type"] = "image/jpeg"
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
