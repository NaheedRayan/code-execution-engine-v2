FROM ubuntu:20.04 

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y

# RUN adduser --disabled-password --gecos "" judge

# for gcc 
RUN apt install curl vim build-essential -y

# for jdk
RUN apt-get install openjdk-8-jdk -y

# for dart
RUN apt-get install wget
RUN apt-get install apt-transport-https
RUN wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/dart.gpg
RUN echo 'deb [signed-by=/usr/share/keyrings/dart.gpg arch=amd64] https://storage.googleapis.com/download.dartlang.org/linux/debian stable main' | tee /etc/apt/sources.list.d/dart_stable.list
RUN apt-get update
RUN apt-get install dart


RUN curl -sL https://deb.nodesource.com/setup_14.x | bash 
RUN apt-get install nodejs -y
# RUN apt install npm -y

# Create app directory
WORKDIR /usr/src/app


# copying everything from the app dir to the working dir
COPY ./app .

# installing the dependencies in the working dir
RUN npm install

# making a temp folder in working dir
RUN mkdir temp

# # exposing port 3000
# EXPOSE 3000

# running the worker
CMD [ "node" , "app.js" ]