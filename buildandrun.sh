#!/usr/bin/env bash
docker build -t py_ai_gps . 
docker run -it --rm --name py_ai_gps -p 8080:80 py_ai_gps