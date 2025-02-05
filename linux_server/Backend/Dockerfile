FROM python:3.10-slim

RUN apt-get update && apt-get install -y espeak alsa-utils

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5100

CMD ["python", "LinuxServer.py"]