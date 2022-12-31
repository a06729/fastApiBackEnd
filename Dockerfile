FROM python:3.11

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

RUN pip3.11 install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]