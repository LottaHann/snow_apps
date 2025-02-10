from queue import Queue, Empty
from flask import Flask, Response, render_template, request
from flask_cors import CORS
import time
import requests
import copy
import jsonify

app = Flask(__name__, static_url_path='/FaceLibrary', static_folder='FaceLibrary', template_folder='FaceProject')
app.debug = False
CORS(app)
queue = Queue()
server_url = "http://172.17.0.2:8008" #detection server url, how to know automtically?

def get_eye_coordinates():
    try:
        response = requests.get(server_url+"/see")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        # This will catch any request-related errors
        print(f"An error occurred: {e}")
        data = []  # Set data to an empty list or handle the error as needed
    
    
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict) and 'spatialCoordinates' in first_item:
            coordinates = first_item['spatialCoordinates']
            x = coordinates['x']
            y = coordinates['y']
            # Process the coordinates as needed
            return {'x_cord': x, 'y_cord': y}
    
    return {'x_cord': 0, 'y_cord': 0}

def modify_eye_path(face):
    new_face = copy.deepcopy(face)

    base_coordinates = {
        'eye_left': {'x': 121.33035, 'y': 159.60567},
        'eye_right': {'x': 203.91816, 'y': 159.79463},
        'eb_left': {'x': 85.422617, 'y': 126.15477},
        'eb_right': {'x': 169.90029, 'y': 126.15476},
        'mouth': {'x': 97.3423, 'y': 213.19999}  
    }



    face_eye_left_string = face['eye_left']
    face_eye_right_string = face['eye_right']
    eye_left_x = 121.33035
    eye_left_y = 159.60567
    eye_right_x = 203.91816
    eye_right_y = 159.79463

    new_coordinates = get_eye_coordinates()
    # Define multipliers for eyes and other elements
    eye_multiplier_x = -0.15
    eye_multiplier_y = -0.12
    face_multiplier_x = -0.1
    face_multiplier_y = -0.1
    
    # Calculate offsets
    eye_x_offset = float(new_coordinates['x_cord']) * eye_multiplier_x
    eye_y_offset = float(new_coordinates['y_cord']) * eye_multiplier_y
    face_x_offset = float(new_coordinates['x_cord']) * face_multiplier_x
    face_y_offset = float(new_coordinates['y_cord']) * face_multiplier_y
    
    # Modify each element
    for element, base in base_coordinates.items():
        element_string = face[element]
        if element.startswith('eye'):
            # Apply larger offsets to eyes
            modified_string = element_string.replace(
                str(base['x']), str(base['x'] + eye_x_offset)
            ).replace(
                str(base['y']), str(base['y'] + eye_y_offset)
            )
        else:
            # Apply smaller offsets to other elements
            modified_string = element_string.replace(
                str(base['x']), str(base['x'] + face_x_offset)
            ).replace(
                str(base['y']), str(base['y'] + face_y_offset)
            )
        new_face[element] = modified_string

    return new_face

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