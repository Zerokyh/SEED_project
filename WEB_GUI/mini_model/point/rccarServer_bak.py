#!/usr/bin/env python3

import cv2
import rospy
import subprocess
import os
import sys
import signal
import pyzbar.pyzbar as pyzbar
from point1_test import *
from ast import And
from cProfile import run
from flask import Flask, Response, request, render_template
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult
# from controlServer import *

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
if cam.isOpened()==False:
   print("cant open cam")
   exit()
cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

app = Flask(__name__, template_folder=".")

x = 0
y = 0
theta = 0

def generate():
    while True:
        global strings
        ret, image = cam.read()
        decodedObjects = pyzbar.decode(image)
        jpegdata=cv2.imencode(".jpeg",image)[1].tobytes()
        string = "--MjpgBound\r\n"
        string += "Content-Type: image/jpeg\r\n"
        string += "Content-length: "+str(len(jpegdata))+"\r\n\r\n"
        yield (string.encode("utf-8") + jpegdata + "\r\n\r\n".encode("utf-8"))

        for obj in decodedObjects:
            qr=obj.data.decode()
            strings = qr.split()
            # print(strings)
            
            global x, y, theta
            x = float(strings[0])
            y = float(strings[1])
            theta = float(strings[2])
        
# stream camera
@app.route('/stream')
def do_stream():
   return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=--MjpgBound')

#control rccar
@app.route('/navi', methods=['POST'])
def control_rccar():
    command=request.form.get('command')
    print(command)
    
    global x, y, theta

    if command == "P1":
        x = 2.3
        y = 1.4
        theta = 0
        print(x, y, theta)

    elif command == "P2":
        x = 0.14
        y = 0.02
        theta = 0
        print(x, y, theta)    
        
    elif command == "P3":
        x = 0.27
        y = 0.32
        theta = 0
        print(x, y, theta)
        
    elif command == "A1":
        x = 2.58
        y = 0.73
        theta = 0
        print(x, y, theta)

    elif command == "A2":
        x = 0.25
        y = 0.24
        theta = 0
        print(x, y, theta)
        
    elif command == "A3":
        x = 0.27
        y = 0.3
        theta = 0
        print(x, y, theta)
       
    elif command == "GO" :
        GO(x, y, theta)
    
    elif command == "STOP":     STOP()
    
    elif command == "RESET":    STOP(), RESET()
        
    return ''

def handler(signal, frame):
    print('\nCtrl + C is detected! Shutdown the server.')
    sys.exit(0)
    
signal.signal(signal.SIGINT, handler)

#remote control
@app.route('/')
def do_route():
    return render_template("index_1.html")

# navigation control
# @app.route('/')
# def do_route():
#     return render_template("index_1.html")

# basic
# @app.route('/working')
# def working():
#     return render_template("working.html")

# point
@app.route('/working')
def working():
    global x, y, theta
    point = x, y, theta
    return render_template("working.html", point=point)

@app.route('/follow')
def follow():
    return render_template("follow.html")

if __name__ =='__main__':
    #initMotors()
    app.run(host='192.168.123.79', port=8080)


        
