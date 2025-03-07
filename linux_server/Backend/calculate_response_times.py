import re
from datetime import datetime

def parse_log(log_lines):
    entries = []
    print("nr of log_lines: " + str(len(log_lines)))
    for line in log_lines:
        split_line = line.split(", ")
        #print("split_line: " + str(split_line))
        if len(split_line) < 2:
            continue

        entry = {}

        if split_line[0] == 'Type: text':
            #print("Text")
            entry["Type"] = "text"
            entry["Question received"] = split_line[1].split(": ")[1]
            entry["Answer played"] = split_line[2].split(": ")[1]
            entry["cal ended"] = split_line[3].split(": ")[1]
        else:
            #print("Speech")
            entry["Type"] = "speech"
            for i in range(0, len(split_line)):
                part = split_line[i]
                #print("part: " + part)
                if ":" in part:
                    key, value = part.split(": ")
                    if key == "received status":
                        key = value
                        value = split_line[i+1].split(": ")[1]
                    elif key == "at time":
                        continue
                    
                    entry[key] = value

        entries.append(entry)

    #print(entries)
    return entries

def calculate_durations(entries):
    on_to_listen_times = []
    off_to_answer_times = []
    unanswered_questions = 0
    text_question_times = []

    print("len of entries: " + str(len(entries)))

    #amount of speech entries:
    count = sum(1 for d in entries if d.get('Type') == 'speech')
    print(count)
    
    
    for entry in entries:
        #print(entry)
        if entry.get("Type") == "speech":
            if "on" in entry and "Started listening" in entry:
                t1 = datetime.strptime(entry["on"], "%Y-%m-%d %H:%M:%S")
                #print(t1)   
                t2 = datetime.strptime(entry["Started listening"], "%Y-%m-%d %H:%M:%S")
                #print(t2)
                on_to_listen_times.append((t2 - t1).total_seconds())
            
            if "off" in entry and "Answer played" in entry:
                t1 = datetime.strptime(entry["off"], "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(entry["Answer played"], "%Y-%m-%d %H:%M:%S")
                off_to_answer_times.append((t2 - t1).total_seconds())
            
            if "Question received" in entry and "Answer played" not in entry:
                unanswered_questions += 1
        
        elif entry.get("Type") == "text":
            #print("text entry: " + str(entry))
            if "Question received" in entry and "Answer played" in entry:
                t1 = datetime.strptime(entry["Question received"], "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(entry["Answer played"], "%Y-%m-%d %H:%M:%S")
                text_question_times.append((t2 - t1).total_seconds())
    
    return on_to_listen_times, off_to_answer_times, unanswered_questions, text_question_times

# Read log file
with open("response_times.log", "r") as file:
    log_lines = file.readlines()

#print(log_lines)
entries = parse_log(log_lines)
#print(entries)
datatype = type(entries)
#print(datatype)
on_listen, off_answer, unanswered, text_times = calculate_durations(entries)
average_time_between_on_listen = sum(on_listen) / len(on_listen)
average_time_between_off_answer = sum(off_answer) / len(off_answer)
average_text_time = sum(text_times) / len(text_times)

print("Time between 'on' and 'Started listening':", on_listen)
print("Time between 'off' and 'Answer played':", off_answer)
print("Unanswered questions:", unanswered)
print("Time for text questions to be answered:", text_times)
print("Average time between 'on' and 'Started listening':", average_time_between_on_listen)
print("Average time between 'off' and 'Answer played':", average_time_between_off_answer)
print("Average time for text questions to be answered:", average_text_time)

""" OUTPUT
Time between 'on' and 'Started listening': [2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0]
Time between 'off' and 'Answer played': [28.0, 30.0, 18.0, 18.0, 19.0, 126.0, 18.0]
Unanswered questions: 3
Time for text questions to be answered: [12.0, 12.0, 13.0, 11.0, 12.0, 12.0, 12.0, 12.0, 12.0, 13.0, 12.0, 12.0, 13.0, 20.0, 12.0, 12.0, 13.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 13.0]
Average time between 'on' and 'Started listening': 1.5
Average time between 'off' and 'Answer played': 36.714285714285715
Average time for text questions to be answered: 12.48"""
