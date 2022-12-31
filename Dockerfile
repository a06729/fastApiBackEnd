FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get install -y git

RUN git clone https://github.com/davisking/dlib

WORKDIR /dlib
RUN pip3.11 install cmake
RUN python3.11 setup.py install

WORKDIR /app

COPY ./* /app/
COPY ./router/* /app/router/

RUN mkdir -p /app/images
RUN mkdir -p /app/lipsImages

RUN pip3.11 install --no-cache-dir --upgrade -r /app/requirements.txt

RUN groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python




USER python:python

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]