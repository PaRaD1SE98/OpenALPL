FROM python:3.9.5-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install libglib2.0-0 libgl1-mesa-glx -y

WORKDIR /app

COPY . /app

RUN pip install -r requirements/docker/production.txt -i https://pypi.tuna.tsinghua.edu.cn/simple