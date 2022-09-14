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
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

db = mysql.connector.connect(
    host="localhost",
    user="asdf",
    passwd="qwer",
    database="test"
)
# from controlServer import *

ab=""
ac=""

cam=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
# if cam.isOpened()==False:
#    print("cant open cam")
#    exit()
cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

app = Flask(__name__, template_folder=".")
x = 0
y = 0
theta = 0
def generate():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM product")
    abc=cursor.fetchall()
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
            global n,id, ac
            qr=obj.data.decode()
            strings = qr.split()
            print(strings)
            global x,y,theta
            x = float(strings[0])
            y = float(strings[1])
            theta = float(strings[2])
            
            n = int(strings[3])
            id = int(strings[4])
            
        # print(x, y, theta)
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


# x = 0
# y = 0
# theta = 0

#control rccar
@app.route('/navi', methods=['POST'])
def control_rccar():
    command=request.form.get('command')
    print(command)
    
    # print(command)
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
        
    # elif command == "QR":
    #     x = float(strings[0])
    #     y = float(strings[1])
    #     theta = float(strings[2])
    #     print(x, y, theta)
    
    elif command == "GO" :
        GO(x, y, theta)
    
    elif command == "STOP":     STOP()
    
    elif command == "RESET":    STOP(), RESET()
           
    return ''

@app.route('/qrdb', methods=['POST'])
def dbt():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM product")
    abc=cursor.fetchall()
    global strings
    global n
    global ab
    global id
    global ac
    # p = pool(initializer=init)
    command=request.form.get('command')
    up_sql= "update product set 재고량 = 재고량+%s where id = %s"
    dw_sql= "update product set 재고량 = 재고량-%s where id = %s"
    # print(command)
    if command == "1":
        n=1
        # cursor.execute(up_sql,aa)
    elif command == "2":
        n=2
    elif command == "3":
        n=3
    elif command == "4":
        n=4
    elif command == "5":
        n=5
    elif command == "6":
        n=6
    elif command == "id_1-1":
        ac=""
        ab=""
        id = 1
        ab=abc[0][1]
        if abc[0][4] < abc[0][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
    elif command == "id_1-2":
        ab=""
        ac=""
        id=2
        ab=abc[1][1]
        if abc[1][4] < abc[1][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
    elif command == "id_1-3":
        ab=""
        ac=""
        id=3
        ab=abc[2][1]
        if abc[2][4] < abc[2][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
        # cursor.execute(up_sql,aa)
    elif command == '입고':
        # conn = connection()
        # cursor = db.cursor(buffered=True)
        # sel_sql1 = "select * from product"
        # cursor.execute("SELECT * FROM product")
        # up_sql= "update product set stock = stock+%s where id = %s"
        # aaa=(strings[0],'2')
        aa=(n,id)
        cursor.execute(up_sql,aa)
        # cursor.execute("update product set stock = stock+%s where id =2;", int(strings[0]))
        db.commit()
    elif command == '출고':
        # cursor.execute("SELECT * FROM product")
        # cursor.execute("update product set stock = stock-1 where id = 'xx';")
        aa=(n,id)
        cursor.execute(dw_sql,aa)
        # bbb=('ID')
        db.commit()
    return ""

# def qr():
#     command=request.form.get('command')
#     print(command)
    
#     global x, y, theta
    
#     if command == "QR":
#         x = float(strings[0])
#         y = float(strings[1])
#         theta = float(strings[2])
#         print(x, y, theta)
    
#     elif command == "GO" :
#         GO(x, y, theta)

def handler(signal, frame):
    print('\nCtrl + C is detected! Shutdown the server.')
    sys.exit(0)
    
signal.signal(signal.SIGINT, handler)

#remote control
@app.route('/')
def do_route():
    return render_template("index_1.html")

@app.route('/dbserver')
def main():
    global cursor
    global ab
    global x
    cars = []
    # conn = connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM product")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "제품명": row[1], "좌표": row[2], "안전재고": row[3], "재고량": row[4], "생성일시": row[5]})
        
    
    return render_template("dbserver.html", cars = cars, acc=ab, ac=ac)

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
    app.run(host='0.0.0.0', port=8080)


        
