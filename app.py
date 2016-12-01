import os
from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))


@app.route("/")
def index():
    return render_template("index.html")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n"b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
