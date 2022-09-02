
# from flask import Flask, render_template
from flask import Flask, Response, request, render_template
# import pymysql
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import cv2
import pyzbar.pyzbar as pyzbar
# import beautifulsoup
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

# cam=cv2.VideoCapture(0)
# font = cv2.FONT_HERSHEY_PLAIN
# if cam.isOpened()==False:
#    print("cant open cam")
#    exit()
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)

# def generate():
#     while True:
#         global strings
#         ret, image = cam.read()
#         decodedObjects = pyzbar.decode(image)
#         jpegdata=cv2.imencode(".jpeg",image)[1].tobytes()
#         string = "--MjpgBound\r\n"
#         string += "Content-Type: image/jpeg\r\n"
#         string += "Content-length: "+str(len(jpegdata))+"\r\n\r\n"
#         yield (string.encode("utf-8") + jpegdata + "\r\n\r\n".encode("utf-8"))

#         for obj in decodedObjects:
#             qr=obj.data.decode()
#             strings = qr.split()
#             print(strings[0])
            

# @app.route('/stream')
# def do_stream():
#    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=--MjpgBound')

# pool = None
# def init():
#     global pool
#     pool = MySQLConnectionPool(...)

# @app.route('/qrdb', methods=['POST'])

#연결된 db하나의 인덱스로 한개씩 불러오기
# @app.route('/')
# def main():
#     command=request.form.get('command')
#     global cursor
#     global id
#     global ab
#     add=ab
#     cars = []
#     # conn = connection()
#     cursor = db.cursor(buffered=True)
#     cursor.execute("SELECT * FROM product")
#     for row in cursor.fetchall():
#         cars.append({"id": row[0], "제품명": row[1], "좌표": row[2], "안전재고": row[3], "재고량": row[4], "생성일시": row[5]})
#     # db.close()
#     # if command == "id_1-1":
#     #     id = '1'
#     #     ab=cursor[0][1]
#     #     print(ab)
#     # elif command == "id_1-2":
#     #     id='2'
#     #     ab=cursor[1][1]
#     # elif command == "id_1-3":
#     #     id='3'
#     #     ab=cursor[2][1]
    
#     return render_template("carsales.html", cars = cars,add=add)

ab=""



    
@app.route('/qrdb', methods=['POST'])
def dbt():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM product")
    global strings
    global x
    global ab
    global id
    abc=cursor.fetchall()
    # p = pool(initializer=init)
    command=request.form.get('command')
    up_sql= "update product set 재고량 = 재고량+%s where id = %s"
    dw_sql= "update product set 재고량 = 재고량-%s where id = %s"
    # print(command)
    if command == "1":
        x=1
        # cursor.execute(up_sql,aa)
    elif command == "2":
        x=2
    elif command == "3":
        x=3
    elif command == "4":
        x=4
    elif command == "5":
        x=5
    elif command == "6":
        x=6
    elif command == "id_1-1":
        id = 1
        ab=abc[0][1]
    elif command == "id_1-2":
        id=2
        ab=abc[1][1]
    elif command == "id_1-3":
        id=3
        ab=abc[2][1]
        # cursor.execute(up_sql,aa)
    elif command == '입고':
        # conn = connection()
        # cursor = db.cursor(buffered=True)
        # sel_sql1 = "select * from product"
        # cursor.execute("SELECT * FROM product")
        # up_sql= "update product set stock = stock+%s where id = %s"
        # aaa=(strings[0],'2')
        aa=(x,id)
        cursor.execute(up_sql,aa)
        # cursor.execute("update product set stock = stock+%s where id =2;", int(strings[0]))
        db.commit()
    elif command == '출고':
        # cursor.execute("SELECT * FROM product")
        # cursor.execute("update product set stock = stock-1 where id = 'xx';")
        aa=(x,id)
        cursor.execute(dw_sql,aa)
        # bbb=('ID')
        db.commit()
    return ""
    # return ""
        
# def main():
#     cars = []
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM product")
#     for row in cursor.fetchall():
#         cars.append({"id": row[0], "name": row[1], "location": row[2], "stock": row[3]})
#     conn.close()
#     return render_template("carsales.html", cars = cars)

@app.route('/')
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
    # db.close()
    # if command == "id_1-1":
    #     id = '1'
    #     ab=cursor[0][1]
    #     print(ab)
    # elif command == "id_1-2":
    #     id='2'
    #     ab=cursor[1][1]
    # elif command == "id_1-3":
    #     id='3'
    #     ab=cursor[2][1]
    acc=ab
    return render_template("carsales.html", cars = cars, acc=acc)

if(__name__ == "__main__"):
    app.run()