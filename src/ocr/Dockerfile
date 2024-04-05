# ocr/Dockerfile

FROM python:3.10.2-slim-bullseye

WORKDIR /wd

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 poppler-utils -y
# RUN apt-get update && apt-get install poppler-utils -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /wd