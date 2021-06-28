FROM python:3.9.5

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install libgl1-mesa-glx -y

WORKDIR /app

COPY . /app

RUN pip install -r requirements/docker/production.txt -i https://pypi.tuna.tsinghua.edu.cn/simple