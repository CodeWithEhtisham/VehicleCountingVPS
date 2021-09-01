#!/usr/bin/python3
from flask import Flask, Response, render_template, request, jsonify
import json
import datetime
from PIL import Image
import io
import sqlite3
# from servsocket import Streaming_Video
import base64
import numpy as np
import pandas as pd
import time
# import sys
# import os
# from utils import getter,setter
app = Flask(__name__)
# global flags 
flags=False
waiting=True
# stream = Streaming_Video('0.0.0.0', 5555)


# def gen(status=False):
#         print("start status ,",status)
#         global stream
#         # global counterFlag
       
        
#         while True:
#             # print("app counter flag ",getter())
#             if getter():
#                 # del stream
#                 # os.execv(__file__, sys.argv)
#                 # stream.stop()
#                 print("if true")
#                 # stream = Streaming_Video('0.0.0.0', 5555)
#                 stream.start()
                
#                 setter(False)
#                 print(getter())
#             if stream.streaming:
#             # frame=pickle.loads(stream.get_jpeg(), fix_imports=True, encoding="bytes")
#             # print(frame)
#             # frame = frame.decode()
#             # print('frame',frame[0:100])
#             # img_conv = base64.b64decode(frame)
#             # as_np = np.frombuffer(img_conv, dtype=np.uint8)
#             # org_im = cv2.imdecode(as_np,flags=1)
#             # yield(org_im)
#             # print("frame",stream.get_jpeg())
#             # print("sleep")
#                 f = open('2.jpg', 'wb')
#                 f.write(stream.get_jpeg())
#                 f.close()
#                 # print(type(stream.get_jpeg()))
#                 # image=Image.open(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream.get_jpeg() + b'\r\n\r\n')
#                 # image.save(r"img")
#                 # time.sleep(4)
#                 yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream.get_jpeg() + b'\r\n\r\n')
#                 print("status   ",status)
#                 # if status==False:
#                 #     print("stop stream")
#                 #     stream.stop()
#                 #     del stream
#                 # else:
#                 #     print("continue stream")
#                 #     continue
# streams=gen(True)


def fetchDataframe(limit=100):
    con = sqlite3.connect("database.db")
    mycursor = con.cursor()
    
    # code to split it into 2 lists
    # res1, res2 = map(list, zip(*ini_list))
    if limit != 1:
        mycursor.execute(
        "SELECT * from data LEFT JOIN results ON data.frame_id=results.frame_id ORDER by data.frame_id desc limit {}".format(limit))
        result = mycursor.fetchall()
        con.close()
        df = pd.DataFrame({
            "date": [i[2] for i in result],
            "frame_id": [i[4] for i in result],
            "tag":[i[3] for i in result],
            "vehicle": [i[5] for i in result],
            "id": [i[5] for i in result],
            "lable": [i[7] for i in result]})
        # print(result)
        return df
    else:
        mycursor.execute(
            "SELECT * FROM data ORDER BY data.frame_id desc LIMIT {}".format(limit)
        )
        result=mycursor.fetchall()[0]
        tag=result[-2]
        # print(result[-2])
        # print(result)
        mycursor.execute(
            "SELECT * FROM results where results.frame_id={}".format(result[-1])

        )
        result=mycursor.fetchall()
        con.close()
        dic={
            "Car":0,
            "Bus":0,
            "Truck":0,
            "rikshaw":0,
            "Bike":0,
            "Van":0,
            "total":0

        }
        for i in result:
            # print(i["label"])
            if i[2] =='Motorcycle' or i[2]=="Bicycle":
                dic['Bike']+=1
                dic['total']+=1
            elif i[2]=='Auto_rikshaw':
                dic['rikshaw']+=1
                dic['total']+=1
            elif i[2]=='Bus':
                dic['Bus']+=1
                dic['total']+=1
            elif i[2]=='Truck':
                dic['Truck']+=1
                dic['total']+=1
            elif i[2]=='Van':
                dic['Van']+=1
                dic['total']+=1
            else:
                dic['Car']+=1
                dic['total']+=1

        return json.dumps(dic),tag
        # return result
    # return df

def data_check(df, name):
    try:
        return df[name]
    except:
        return 0

def bar_data(df):
    df = df.lable.value_counts()
    # print(data_check(df, "Motorcycle"))
    # print(type(data_check(df, "Motorcycle")))
    return [
        [1, data_check(df, 'Car')],
        [2, data_check(df, "Bus")],
        [3, data_check(df, "Motorcycle") + data_check(df, "Bicycle") ],
        [4, data_check(df, "Van")],
        [5, data_check(df, "Truck")],
        [6, data_check(df, "Auto_rikshaw")]
        # [7, data_check(df, "Auto_rikshaw")]
    ]

def donut_data(df):
    df = df.lable.value_counts()
    s = sum(df.values)
    if s == 0:
        s = 1
    return [
        {
            'label': 'Car',
            'data': int((data_check(df, "Car")/s)*100),
            'color': '#3c8dbc'
        },
        {
            'label': 'Bus',
            'data': int((data_check(df, "Bus")/s)*100),
            'color': '#0073b7'
        },
        {
            'label': 'Truck',
            'data': int((data_check(df, "Truck")/s)*100),
            'color': '#737CA1'
        },
        {
            'label': 'Bike',
            'data': int((data_check(df, "Bike")/s)*100) + int((data_check(df, "Bicycle")/s)*100),
            'color': '#6D7B8D'
        },
        # {
        #     'label': 'Cycle',
        #     'data': int((data_check(df, "Bicycle")/s)*100),
        #     'color': '#566D7E'
        # },
        {
            'label': 'Rikshaw',
            'data': int((data_check(df, "Auto_rikshaw")/s)*100),
            'color': '#00c0ef'
        },
        {
            'label': "Van",
            'data': int((data_check(df, "Van")/s)*100),
            'color': '#6D7B8D'
        }

    ]

def line_plot(df):
    dt = df[['date', 'id']].groupby(by='date').count()
    d = pd.DatetimeIndex(dt.index)
    year, month, day, hour, minute, second = [], [], [], [], [], []

    for i in d:
        # Y = i.year
        # M = i.month
        # D = i.day
        # h = i.hour
        # m = i.minute
        # s = i.second
        year.append(i.year)
        month.append(i.month)
        day.append(i.day)
        hour.append(i.hour)
        minute.append(i.minute)
        second.append(i.second)
    value = [int(i) for i in dt.id.values]
    return year, month, day, hour, minute, second, value, len(dt.id.values)

@app.route("/home", methods=['GET', 'POST'])
def home():
    # try:
    #     del streams
    # except UnboundLocalError:
    #     streams=gen(True)
    # flags=False
    # gen(False)
    return render_template("index.html", jsondata=get_json())
@app.route("/", methods=['GET', 'POST'])
def index():
    # try:
    #     del streams
    # except UnboundLocalError:
    #     streams=gen(True)
    # flags=False
    # gen(False)
    return render_template("index.html", jsondata=get_json())

# @app.route('/video_feed')
# def video_feed():
    
#     print("hello")
#     print("frame ",gen())
#     # print(Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame'))
#     return Response(gen(True), mimetype='multipart/x-mixed-replace; boundary=frame')
# @app.route('/livestream',methods=['GET','POST'])
# def livestream():
#     streams=gen(True)
#     return render_template("livestream.html")

@app.route("/history",methods=["GET","POST"])
def history():
    print("history loading")
    if request.method=="POST":
        # print("post histoyr")
        print("start datetime",request.form['start'])
        return render_template("history.html",jsondata=get_json())
    else:
        print("get histoyr")
        return render_template("history.html")
        
@app.route("/prediction",methods=["GET","POST"])
def prediction():
    # print("prediction loading")
    if request.method=="POST":
        # print("post prediction")
        # print("start datetime",request.form['start'])
        return render_template("prediction.html",jsondata=get_json())
    else:
        print("get prediction")
        return render_template("prediction.html")

def send_result(response=None, error='', status=200):
    if response is None:
        response = {}
    result = json.dumps({'result': response, 'error': error})
    return Response(status=status, mimetype="application/json", response=result)
@app.route('/fetchtable',methods=["POST","GET"])
def get_table_data():

    global waiting
    # waiting=False
    while True:
        # print("************************************************** ({})".format(waiting))
        if waiting==True:
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ({})".format(waiting))
            break
    df,tag=fetchDataframe(1)
    print(df,tag)
    return df

@app.route('/fetchdata', methods=["POST"])
def get_json():
    # print("hello")
    global flags
    global waiting
    # waiting=False
    while True:
        # print("************************************************** ({})".format(waiting))
        if waiting==True:
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ({})".format(waiting))
            break
    if flags == False:
        # print ("flag false statement")
        df = fetchDataframe()
        bar = bar_data(df)
        donut = donut_data(df)
        # print(line_plot(df))
        year, month, day, hour, minute, second, index, ln = line_plot(df)
        flags=True
        return jsonify({
            "bar_data": str(bar),
            "donut_data": donut,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "line_index_data": index,
            'count': str(np.random.random(1)),
            "checkflag":False
        })
    else:
        # print ("flag true statement")
        df = fetchDataframe()
        bar = bar_data(df)
        donut = donut_data(df)
        # print(line_plot(df))
        year, month, day, hour, minute, second, index, ln = line_plot(df)
        return jsonify({
            "bar_data": str(bar),
            "donut_data": donut,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "line_index_data": index,
            'count': str(np.random.random(1)),
            "checkflag":True
        })

def db_data_insertion(data):
    try:
        con = sqlite3.connect("database.db")
        sql = "INSERT INTO data(camera_id,camera_loc,capture_time,image_path) VALUES(?,?,?,?)"
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        # print("insertion seccessfull in data table")
        a = cur.lastrowid
        con.close()
        return a
    except Exception as e:
        print("insertion in data table failed :{}".format(e))

def db_results_insertion(data):
    try:
        con = sqlite3.connect("database.db")
        sql = "INSERT INTO results(frame_id,label,prob,x,y,w,h) VALUES(?,?,?,?,?,?,?)"
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        # print("insertiion seccessfull in results table")
        con.close()
    except Exception as e:
        print("insertion in result table failed :{}".format(e))

@app.route("/upload", methods=['POST'])
def login():
    
    global waiting
    waiting=False
    # print("/////////////////////////////////////////////////////////// ({})".format(waiting))
    if request.method == 'POST':
        try:
            img_str = request.json['image']
            tag = request.json["tag"]
            camera_id = request.json['camera_id']
            camera_loc = request.json['camera_loc']
            date_time=request.json["datetime"]
            results = request.json['results']
            img_byte=base64.b64decode(img_str.encode('utf-8'))
            img=Image.open(io.BytesIO(img_byte))
            img.save(f"static/img/output.jpg")
            # img.save(f"static/img/{tag}.jpg")
            # jpg_original = base64.b64decode(img_str)
            # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            # img = imdecode(jpg_as_np, flags=1)
            frame_id = db_data_insertion(
                (camera_id, camera_loc,date_time , tag))
            # imwrite(f"static/img/output.jpg", img)

            for r in results:
                lbl = r['label']
                prob = r['prob']
                x = r['x']
                y = r['y']
                w = r['w']
                h = r['h']
                db_results_insertion((frame_id, lbl, prob, x, y, w, h))
            waiting=True
            # print("/////////////////////////////////////////////////////////// ({})".format(waiting))


            return send_result("Frame inserted success", status=201)
        except KeyError as e:
            return send_result(error=f'An "image" file is required {e}', status=422)
        except Exception as e:
            return send_result(error=f'Error {e}', status=500)


if __name__ == "__main__":
    # app.run(host="127.0.0.1",threaded=True)
    app.run(host="0.0.0.0",port=4000,threaded=True,debug=True) # home desktop
