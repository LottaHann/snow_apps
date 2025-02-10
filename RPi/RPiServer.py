from queue import Queue, Empty
from flask import Flask, Response, render_template, request
from flask_cors import CORS
import time

app = Flask(__name__, static_url_path='/FaceLibrary', static_folder='FaceLibrary', template_folder='FaceProject')
app.debug = False
CORS(app)
queue = Queue()

@app.route("/")
def frontpage():
    return render_template("index.html")

@app.route("/api/post", methods=["GET", "POST"])
def api_parse_sentence():
    print("received post request...")
    face_data = request.args.get("face")
    if face_data:
        print(f"Received face data: {face_data}")
        queue.put(face_data)
        return "Face OK"
    else:
        print("No face data received")
        return "Invalid request"

def event_stream():
    while True:
        try:
            message = queue.get_nowait()
            print(f"Sending {message}")
            yield f"data: {message}\n\n"
        except Empty:
            time.sleep(0.1)  # Sleep for a short interval to avoid busy-waiting
            continue

@app.route("/api/stream")
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000)

#test