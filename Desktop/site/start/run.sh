#!/bin/bash
app="flask"
sudo docker build -t ${app} .
sudo docker run -d -p 56733:80\
  --name=${app}\
  -v $PWD:/app ${app}
