from queue import Queue
from flask_cors import CORS
from flask import Flask, Response, render_template, request,  jsonify
import requests,os
import socket
from RunListenToVoice import listen_to_voice, get_askRobot, stopCall
# from chatboot.new_test_spacy_bot import get_response

# Hämta nuvarande arbetskatalog
current_directory = os.getcwd()
script_directory = os.path.dirname(os.path.abspath(__file__))

def send_face_data(data,post_name):
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
    try:
        get_askRobot(data)
    except:
        return None
    
def runCalling(input):
    print(input)
    if input == "off":
        stopCall()
        print(input)
        return None
    try:
        listen_to_voice()
    except:
        return input

# app = Flask(__name__)
app = Flask(__name__)
app.debug = False
CORS(app)
queue = Queue()

@app.route("/")
def frontpage():
    ip = request.environ.get("HTTP_HOST", "Unknown")
    expression_ip = request.environ.get("REMOTE_ADDR", "Unknown")
    test = expression_ip
    expression_ip = expression_ip + ""
    # expression_ip =  5100
    # HTTP_HOST=  192.168.32.6:5100
    
    return render_template("index.html", expression_ip=test, ip=ip)

@app.route("/api/post", methods=["GET"])
def api_parse_sentence():
    face_data = request.args.get("face")
    touch_data = request.args.get("touch")
    call_data = request.args.get("call")
    textToSpeech_data= request.args.get("text")
    
    if face_data:
        queue.put(face_data)
        send_face_data(face_data,"face")
        return "Face OK"
    elif touch_data:
        queue.put(touch_data)
        send_face_data(touch_data,"touch")
        return "Touch OK"
    elif call_data:
        print("call_data")
        queue.put(call_data)
        runCalling(call_data)
        return "call ok"
    elif textToSpeech_data:
        queue.put(textToSpeech_data)
        text_to_speech(textToSpeech_data)
      
        return "TTS OK"
    else:
        return "Invalid request"
      
if __name__ == '__main__':
    app.run(threaded=False,host='0.0.0.0', port=5100)