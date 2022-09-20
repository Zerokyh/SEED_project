#!usr/bin/python

from flask import Flask, Response, request, render_template
import cv2
#from controlServer import *

# cam=cv2.VideoCapture(0)
# if cam.isOpened()==False:
#    print("cant open cam")
#    exit()
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

app = Flask(__name__, template_folder=".")

def generate():
   while True:
       ret, image = cam.read()
       jpegdata=cv2.imencode(".jpeg",image)[1].tobytes()
       string = "--MjpgBound\r\n"
       string += "Content-Type: image/jpeg\r\n"
       string += "Content-length: "+str(len(jpegdata))+"\r\n\r\n"
       yield (string.encode("utf-8") + jpegdata + "\r\n\r\n".encode("utf-8"))
        
#stream camera
@app.route('/stream')
def do_stream():
   return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=--MjpgBound')

#control rccar
@app.route('/motor', methods=['POST'])
def control_rccar():
    command=request.form.get('command')
    print(command)
    if command == "GO": forward()
    elif command == "LEFT": left()
    elif command == "STOP":  stop()
    elif command == "RIGHT": right()
    elif command == "BACK": backward()
    return ''
    
@app.route('/')
def do_route():
    return render_template("index.html")

#@app.route('/working')
#def working():
    #return render_template("working.html")

#@app.route('/follow')
#def follow():
    #return render_template("follow.html")


if __name__ =='__main__':
    # initMotors()
    #app.run(host='192.168.0.179', port=8080)
    app.run(host='192.168.123.79', port=8080)
    #app.run(host='localhost', port=8080)

