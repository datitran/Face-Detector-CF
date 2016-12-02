(function() {
    "use strict";

    function FaceDetector(videoId, grabCanvasId, outputImgId) {
        this.video = document.getElementById("pretty_faces");
        this.canvas = document.getElementById("framegrab");
        this.canvasCtx = this.canvas.getContext("2d");
        this.faces = document.getElementById("faces");
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

                self.scheduleFrameGrab();
            });
        },

        scheduleFrameGrab: function() {
            var self = this;

            window.setTimeout(function() {
                self.grabFrame();
            }, 1000);
        },

        grabFrame: function() {
            var self = this;

            this.canvasCtx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            this.canvas.toBlob(function(imageData) {
                var postImageReq = new XMLHttpRequest();
                postImageReq.open("POST", "/prediction", true);
                postImageReq.responseType = "arraybuffer";

                postImageReq.onload = function(event) {
                    var imageBlob = new Blob([postImageReq.response], {type: "image/jpeg"});
                    self.url = URL.createObjectURL(imageBlob);

                    faces.addEventListener("onload", function() {
                        console.log("revoking url");
                        URL.revokeObjectURL(self.url);
                    });
                    self.faces.src = self.url;
                };

                postImageReq.send(imageData);
            }, "image/jpeg", 70);

            this.scheduleFrameGrab();
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