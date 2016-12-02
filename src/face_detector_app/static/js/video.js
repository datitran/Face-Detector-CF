(function() {
    "use strict";

    function FaceDetector(videoId, grabCanvasId, outputCanvasId) {
        this.video = document.getElementById(videoId);
        this.canvas = document.getElementById(grabCanvasId);
        this.canvasCtx = this.canvas.getContext("2d");
        this.rectangles = document.getElementById(outputCanvasId);
        this.rectanglesCtx = this.rectangles.getContext("2d");
    }

    FaceDetector.prototype = {
        start: function() {
            var constraints = window.constraints = {
                audio: false,
                video: true
            };
            var self = this;

            navigator.mediaDevices
                .getUserMedia(constraints)
                .then(function(stream) {
                    self.handleSuccess(stream);
                }).catch(function(error) {
                    self.handleError(error);
                });

            this.video.addEventListener("canplay", function() {
                self.canvas.width = self.video.videoWidth;
                self.canvas.height = self.video.videoHeight;
                self.rectangles.width = self.video.videoWidth;
                self.rectangles.height = self.video.videoHeight;

                self.scheduleFrameGrab();
            });
        },

        scheduleFrameGrab: function() {
            var self = this;

            window.setTimeout(function() {
                self.grabFrame();
            }, 500);
        },

        grabFrame: function() {
            var self = this;

            this.canvasCtx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            this.canvas.toBlob(function(imageData) {
                var postImageReq = new XMLHttpRequest();
                postImageReq.open("POST", "/prediction", true);
                postImageReq.responseType = "json";

                postImageReq.onload = function(event) {
                    var faces = postImageReq.response.faces;

                    self.drawFaces(faces);
                    self.scheduleFrameGrab();
                };

                postImageReq.send(imageData);
            }, "image/jpeg", 70);

        },

        drawFaces: function(faces) {
            this.rectanglesCtx.clearRect(0, 0, this.rectangles.width, this.rectangles.height);

            for (var i=0; i<faces.length; i++) {
                this.drawFace(faces[i]);
            }
        },

        drawFace: function(coordinates) {
            var x = coordinates[0],
                y = coordinates[1],
                w = coordinates[2],
                h = coordinates[3];

            this.rectanglesCtx.strokeStyle = "green";
            this.rectanglesCtx.lineWidth = 2;
            this.rectanglesCtx.strokeRect(x, y, w, h);
        },

        handleSuccess: function(stream) {
            var videoTracks = stream.getVideoTracks();
            console.log('Got stream with constraints:', constraints);
            console.log('Using video device: ' + videoTracks[0].label);
            stream.oninactive = function() {
                console.log('Stream inactive');
            };
            window.stream = stream; // make variable available to browser console

            this.video.srcObject = stream;
        },

        handleError: function(error) {
            if (error.name === 'ConstraintNotSatisfiedError') {
                this.errorMsg('The resolution ' + constraints.video.width.exact + 'x' +
                    constraints.video.width.exact + ' px is not supported by your device.');
            } else if (error.name === 'PermissionDeniedError') {
                this.errorMsg('Permissions have not been granted to use your camera and ' +
                    'microphone, you need to allow the page access to your devices in ' +
                    'order for the demo to work.');
            }
            this.errorMsg('getUserMedia error: ' + error.name, error);
        },

        errorMsg: function(msg, error) {
            var errorElement = document.getElementById("error");
            errorElement.innerHTML += '<p>' + msg + '</p>';
            if (typeof error !== 'undefined') {
                console.error(error);
            }
        }
    };

    window.FaceDetector = FaceDetector;
}())