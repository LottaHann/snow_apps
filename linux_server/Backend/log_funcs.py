
def log_audio_recognized(time):
    """
    Log the time when audio is recognized.
    
    :param time: The time when audio is recognized.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Audio recognized: {time}, ")

def log_stop_listening(time):
    """
    Log the time when stop_listening is called.
    
    :param time: The time when stop_listening is called.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"stop_listening called at: {time}, ")

def log_callback(time):
    """
    Log the time when the callback function is called.
    
    :param time: The time when the callback function is called.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Callback called at: {time}, ")

def log_search_answer(time):
    """
    Log the time when searching for an answer.
    
    :param time: The time when searching for an answer.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Find answer: {time}, ")

def log_answer_found(time):
    """
    Log the time when an answer is found.
    
    :param time: The time when an answer is found.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Answer found: {time}, ")

def log_started_listening(time):
    """
    Log the time when the system starts listening.
    
    :param time: The time when the system starts listening.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Started listening: {time}, ")

def log_answer_play(answer_time):
    """
    Log the time when the answer is played.
    
    :param answer_time: The time when the answer is played.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Answer played: {answer_time}, ")

def log_call_ended(end_time):
    """
    Log the time when the call ends.
    
    :param end_time: The time when the call ends.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Call ended: {end_time}")


def log_sr_error(time, e):
    """
    Log the time when an error occurs in speech recognition.
    
    :param time: The time when an error occurs in speech recognition.
    :param e: The error message.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"SR error: {time}, {e}, ")



def log_status(status, time):
    """
    Log the status and time.
    
    :param status: The status to log.
    :param time: The time to log.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"received status {status} at time: {time}, ")

def log_type(question_type):
    """
    Log the type of question.
    
    :param question_type: The type of question to log.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"\nType: {question_type}, ")

def log_question_received(question_time):
    """
    Log the time when a question is received.
    
    :param question_time: The time when a question is received.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Question received: {question_time}, ")

def log_transcription_time(time):
    """
    Log the time for transcription.
    
    :param time: The time for transcription.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Transcription time: {time}, ")
        