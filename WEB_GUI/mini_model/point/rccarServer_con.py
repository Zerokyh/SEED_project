#!/usr/bin/env python3

from ast import And
from cProfile import run
from flask import Flask, Response, request, render_template
import cv2
import rospy
# from point1_test import *
from point1_test import *
import subprocess
import os
import sys
import signal
import pyzbar.pyzbar as pyzbar
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult
from controlServer import *

cam=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
if cam.isOpened()==False:
   print("cant open cam")
   exit()
cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

app = Flask(__name__, template_folder=".")

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
            print(strings)
            
            # cv2.putText(string, str(obj.data.decode()), (50, 50), font, 2, (255, 0, 0), 3)
            # rospy.init_node('movebase_client_py')
            # result = movebase_client()
            # if result:
            #     rospy.loginfo("Goal execution done!")
            #     print((sys.version))
            # else: 
            #     rospy.loginfo("Navigation test finished.") 
        # cv2.imshow("Frame", image)
    
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break
    # cam.release()
    # cv2.destroyAllWindows()
#    while True:
    #    ret, image = cam.read()
    #    jpegdata=cv2.imencode(".jpeg",image)[1].tobytes()
    #    string = "--MjpgBound\r\n"
    #    string += "Content-Type: image/jpeg\r\n"
    #    string += "Content-length: "+str(len(jpegdata))+"\r\n\r\n"
    #    yield (string.encode("utf-8") + jpegdata + "\r\n\r\n".encode("utf-8"))
        
# stream camera
@app.route('/stream')
def do_stream():
   return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=--MjpgBound')

# def stop():
#     subprocess.run(['rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'], shell=True)
    
# def STOP():
#     subprocess.run(['roslaunch mini_model emergency_stop.launch'], shell=True)

# def stop():
#         os.system('roslaunch mini_model emergency_stop.launch')

#control rccar
@app.route('/navi', methods=['POST'])
def control_rccar():
    command=request.form.get('command')
    print(command)
    
    global x, y, theta
    if command == "P1":
        x = -0.5
        y = 3.8
        theta = 0
        print(x, y, theta)

    elif command == "P2":
        x = -0.5
        y = 1.8
        theta = 0
        print(x, y, theta)    
        
    elif command == "P3":
        x = -0.5
        y = -1.5
        theta = 0
        print(x, y, theta)
        
    elif command == "A1":
        x = 3.0
        y = 3.8
        theta = 0
        print(x, y, theta)

    elif command == "A2":
        x = 3.0
        y = 1.7
        theta = 0
        print(x, y, theta)
        
    elif command == "A3":
        x = 3.0
        y = 0.2
        theta = 0
        print(x, y, theta)
    
    elif command == "GO" :
        GO(x, y, theta)
    
    elif command == "STOP":     STOP()
    
    elif command == "RESET":    STOP(), RESET()
        
    return ''

def qr():
    command=request.form.get('command')
    print(command)
    global x, y, theta
    
    if command == "QR":
        x = float(strings[0])
        y = float(strings[1])
        theta = float(strings[2])
        print(x, y, theta)
    
    elif command == "GO" :
        GO(x, y, theta)

def handler(signal, frame):
    print('\nCtrl + C is detected! Shutdown the server.')
    sys.exit(0)
    
signal.signal(signal.SIGINT, handler)

#remote control
@app.route('/')
def do_route():
    return render_template("index.html")

# navigation control
# @app.route('/')
# def do_route():
#     return render_template("index_1.html")

# @app.route('/working')
# def working():
    # point = x, y, theta
    # if point==None:
    #     point = 0,0,0
        
    # else:
    #     pass
    
    # render_template("working.html", point=point)
    
# @app.route('/working')
# def working():

#     global x, y, theta, point
    
#     x= 0
#     y=0
#     theta =0
    
#     point = x, y, theta
    
#     # control_rccar(x, y, theta)
#     # point = x, y, theta
#     return render_template("working.html", point=point)

# @app.route('/working')
# def working():
#     point = 0, 0, 0
#     return render_template("working.html", point=point)

@app.route('/working')
def working():
    return render_template("working.html")

@app.route('/follow')
def follow():
    return render_template("follow.html")

if __name__ =='__main__':
    #initMotors()
    app.run(host='192.168.123.79', port=8080)


        
