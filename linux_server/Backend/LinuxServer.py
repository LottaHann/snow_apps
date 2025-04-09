from queue import Queue
from flask_cors import CORS
from flask import Flask, Response, render_template, request,  jsonify
import requests,os
import socket
import time 
from datetime import datetime  
from log_funcs import log_type, log_question_received
from speech_pipeline import respond

# from chatboot.new_test_spacy_bot import get_response

# Hämta nuvarande arbetskatalog
current_directory = os.getcwd()
script_directory = os.path.dirname(os.path.abspath(__file__))
rpi_ip = "192.168.99.200"
expression_server = f'http://{rpi_ip}:5000'



    
def send_face_data(data,post_name):
    """
    Send face data to the expression server.
    
    :param data: The face data to send.
    :param post_name: The name of the post request.
    :return: The response from the server.
    """
    expression_ip = request.environ.get("REMOTE_ADDR")
    try:
        response = requests.get(f'http://{expression_ip}:5000/api/post?face={data}',timeout=0.0000000001)
        print("def:",post_name,data)
        return response
    except requests.exceptions.ReadTimeout: 
        return None
    except requests.RequestException as e:
        print(f"Error sending face data: {e}")
        return None

def text_to_speech(data):
    """
    Convert text to speech.
    
    :param data: The text to convert to speech.
    """
    try:
        respond(data, "text")
    except:
        return None


# app = Flask(__name__)
app = Flask(__name__, template_folder="../Frontend", static_folder="../Frontend/static")
#app = Flask(__name__)
app.debug = False
CORS(app, resources={r"/*": {"origins": [expression_server, "http://localhost:5100", "http://127.0.0.1:5100"]}})
queue = Queue()

@app.route("/")
def frontpage():
    """
    Render the front page.
    
    :return: The rendered front page template.
    """
    ip = request.environ.get("HTTP_HOST", "Unknown")
    expression_ip = request.environ.get("REMOTE_ADDR", "Unknown")
    test = expression_ip
    expression_ip = expression_ip + ""
    # expression_ip =  5100
    # HTTP_HOST=  192.168.32.6:5100
    
    return render_template("index.html", expression_ip=test, ip=ip)

@app.route("/talk_to_snow")
def talk_to_snow():
    """
    Render the talk_to_snow page.
    
    :return: The rendered talk_to_snow page template.
    """
    return render_template("talk_to_snow/index.html")

@app.route("/text_to_snow")
def text_to_snow():
    """
    Render the text_to_snow page.
    
    :return: The rendered text_to_snow page template.
    """
    return render_template("text_to_snow/index.html")

@app.route("/face_expressions")
def face_expressions():
    """
    Render the face_expressions page.
    
    :return: The rendered face_expressions page template.
    """
    return render_template("face_expressions/index.html")

@app.route("/statistics")
def statistics():
    """
    Render the statistics page.
    
    :return: The rendered statistics page template.
    """
    return render_template("statistics/index.html")

@app.route("/talk", methods=["POST"])
def say_text():
    text = request.args.get("text")
    respond(text, "text")
    return "talk ok"

@app.route("/api/post", methods=["GET"])
def api_parse_sentence():
    """
    Parse the incoming API request and handle the data accordingly.
    
    :return: A response indicating the result of the request.
    """
    print("request.args",request.args)
    face_data = request.args.get("face")
    touch_data = request.args.get("touch")
    textToSpeech_data= request.args.get("text")
    
    print("received post request...")

    if face_data:
        queue.put(face_data)
        send_face_data(face_data,"face")
        return "Face OK"
    elif touch_data:
        queue.put(touch_data)
        send_face_data(touch_data,"touch")
        return "Touch OK"
    elif textToSpeech_data:
        log_type("text")
        log_question_received(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        queue.put(textToSpeech_data)
        text_to_speech(textToSpeech_data)
        return "TTS OK"
    else:
        return "Invalid request"
      
if __name__ == '__main__':
    app.run(threaded=False,host='0.0.0.0', port=5100)