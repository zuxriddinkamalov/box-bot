# pull official base image
FROM python:latest

# set work directory
WORKDIR /usr/src/engine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/engine/requirements.txt

# install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/engine/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/engine/
