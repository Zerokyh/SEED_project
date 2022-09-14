
from flask import Flask, Response, request, render_template
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import cv2
import pyzbar.pyzbar as pyzbar

app = Flask(__name__)

# def connection():
#     s = 'localhost' #Your server(host) name 
#     d = 'test' 
#     u = 'asdf' #Your login user
#     p = 'qwer' #Your login password
#     conn = mysql.connector.connect(host=s, user=u, password=p, database=d)
#     return conn

#db연결
db = mysql.connector.connect(
    host="localhost",
    user="asdf",
    passwd="qwer",
    database="test"
)

cam=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
# if cam.isOpened()==False:
#    print("cant open cam")
#    exit()
cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

#html로 보낼 변수 초기화
ab=""
ac=""


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
            n = int(strings[3])
            id = int(strings[4])
         

@app.route('/stream')
def do_stream():
   return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=--MjpgBound')


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
    command=request.form.get('command')
    up_sql= "update product set 재고량 = 재고량+%s where id = %s"
    dw_sql= "update product set 재고량 = 재고량-%s where id = %s"
    if command == "1":
        n=1
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
        id = 1
        ab=abc[0][1]
        if abc[0][4] < abc[0][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
    elif command == "id_1-2":
        id=2
        ab=abc[1][1]
        if abc[1][4] < abc[1][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
    elif command == "id_1-3":
        id=3
        ab=abc[2][1]
        if abc[2][4] < abc[2][3]:
            ac="%s의 재고가 부족합니다" %ab
        else: ac=""
        
    elif command == '입고':
        aa=(n,id)
        cursor.execute(up_sql,aa)
        db.commit()
    elif command == '출고':
        aa=(n,id)
        cursor.execute(dw_sql,aa)
        db.commit()
    return ""

@app.route('/')
def main():
    global cursor
    global ab
    global x
    cars = []
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM product")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "제품명": row[1], "좌표": row[2], "안전재고": row[3], "재고량": row[4], "생성일시": row[5]})
    acc=ab
    return render_template("dbserver.html", cars = cars, acc=acc, ac=ac)

if(__name__ == "__main__"):
    app.run(host='localhost', port=5000)