FROM python:3.8

ENV PYTHONBUFFERED 1

COPY . /opt/project
WORKDIR /opt/project

RUN pip install -U pip
RUN pip install -r requirments.txt -U --no-cache
