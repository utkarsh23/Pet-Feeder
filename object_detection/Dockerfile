# Parent Image (Xenial Xerus)
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get upgrade -y

# Install python3 
RUN  apt-get install -y python3

# Install Compilation Tools
RUN apt-get update
RUN apt-get install -y python3-dev build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
RUN apt-get install -qqy x11-apps

# Install Dependencies Tools
RUN apt-get update 
RUN apt-get install -y wget vim
RUN wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3 /tmp/get-pip.py
RUN pip install --upgrade pip

# Install python Core Packages 
RUN pip install -U numpy
RUN pip install -U matplotlib
RUN pip install -U jupyter
RUN pip install -U pandas
RUN pip install -U Pillow

# Install tensorFlow & keras
RUN pip install -U tensorflow
RUN pip install -U keras

# Install tensorflow's Object Detection Model
RUN git clone https://github.com/tensorflow/models /usr/local/lib/python3.5/dist-packages/tensorflow/models
RUN apt-get install -y python-pil python-lxml python-tk
RUN wget -P /usr/local/src/ https://github.com/google/protobuf/releases/download/v3.6.1/protobuf-python-3.6.1.tar.gz
RUN cd /usr/local/src/ && tar xvf protobuf-python-3.6.1.tar.gz && rm protobuf-python-3.6.1.tar.gz 
RUN cd /usr/local/src/protobuf-3.6.1/ && ./configure && make && make install && ldconfig

# Install OpenCV
RUN apt-get install -y unzip
RUN wget -P /usr/local/src/ https://github.com/opencv/opencv/archive/3.4.3.zip
RUN cd /usr/local/src/ && unzip 3.4.3.zip && rm 3.4.3.zip
RUN cd /usr/local/src/opencv-3.4.3/ && mkdir build
RUN cd /usr/local/src/opencv-3.4.3/build && cmake -D CMAKE_INSTALL_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local/ .. && make -j7 && make install

RUN pip install -U requests

# Setting up working directory 
RUN mkdir /lab
WORKDIR /lab

# Clean And Minimize Image Size 
RUN apt-get autoremove -y
RUN apt-get autoclean -y

# Set tensorflow Environment Variables
ENV PYTHONPATH "$PYTHONPATH:/usr/local/lib/python3.5/dist-packages/tensorflow/models/research:/usr/local/lib/python3.5/dist-packages/tensorflow/models/research/slim"
RUN cd /usr/local/lib/python3.5/dist-packages/tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=.

# Bash Script Containing Python Execution Script
CMD bash docker_execute.sh
