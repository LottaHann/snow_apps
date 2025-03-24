# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

import torch
from transformers import pipeline
from accelerate import infer_auto_device_map
from transformers import AutoModelForCausalLM, AutoTokenizer
import datetime
import ollama
from nltk_model.get_ask import make_ask_response
import json

#model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
#model = AutoModelForCausalLM.from_pretrained(model_name, load_in_8bit=True)
#device_map = infer_auto_device_map(model, max_memory={0: "4GiB", "cpu": "16GiB"})
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map=device_map)

def get_response(input):
    #pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who always responds in a clear and concise manner",
        },
        {"role": "user", "content": input},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return outputs[0]["generated_text"]




def get_response_gpt2(input):
    messages = [
        {"role": "user", "content": input},
    ]
    prompt = input  
    outputs = pipe(prompt, max_new_tokens=50, do_sample=True, temperature=0.7)
    return outputs[0]["generated_text"]

def get_response_granite(input):

    with open("./nltk_model/intents.json", "r", encoding="utf-8") as f:
        context_data = json.load(f)

    #context = make_ask_response(input)
    context = json.dumps(context_data, indent=2)
    print("context: ", context)

    
    messages = [
        {"role": "system", "content": """You are a friendly chatbot who always responds in a clear and concise manner using the context information given.
            question: """},
        {"role": "user", "content": f"""answer the question using the context given:
            context: {context},
            question: {input}
            """},
    ]
    print("message: ", messages)
    
    response = ollama.chat(model="granite3-moe:1b", messages=messages)
    return response["message"]["content"]

def get_response_dolphin(input):
    context = make_ask_response(input)
    print("context: ", context)

    messages = [
        {"role": "system", "content": """You are a friendly chatbot who always responds in a clear and concise manner using the context information given.
            question: """},
        {"role": "user", "content": """answer the question using the context given:
            context: {context},
            question: {input}
            """},
    ]

    print("message: ", messages)
    
    response = ollama.chat(model="granite3-moe:1b", messages=messages)
    return response["message"]["content"]



if __name__ == "__main__":
    pipe = pipeline(
        "text-generation",
        model="gpt2",  # Smallest GPT-2 model
        device="cpu"   # Runs on CPU
    )

    starttime = datetime.datetime.now()
    print("started at ", starttime)
    print(get_response_granite("What is Arcada?"))
    endtime = datetime.datetime.now()

    print("ended at ", endtime)
    print("total time taken: ", (endtime - starttime).total_seconds(), " seconds")
