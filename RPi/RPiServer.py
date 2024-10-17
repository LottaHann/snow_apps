from queue import Queue
from flask import Flask, Response, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='/FaceLibrary', static_folder='FaceLibrary',template_folder='FaceProject')
app.debug = False
CORS(app)
queue = Queue()

@app.route("/")
def frontpage():
	return render_template("index.html")

@app.route("/api/post", methods=["GET"])
def api_parse_sentence():
	queue.put(request.args.get("face"))
	return "OK"

def event_stream():
	while True:
		message = queue.get(True)
		print(f"Sending {message}")
		yield f"data: {message}\n\n"

@app.route("/api/stream")
def stream():
	return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
	app.run(threaded=True ,host='0.0.0.0',  port=5000)