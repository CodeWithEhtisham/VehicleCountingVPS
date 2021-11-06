import cv2
# import matplotlib.pyplot as plt
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import datetime
import time
# import requests
import json
# import base64
import random
import socketio
import cv2
# import time
import base64
sio = socketio.Client()
net=cv2.dnn_DetectionModel("D:\gil\demo\yolov4 vehicle detection\yolov4.cfg","D:\gil\demo\yolov4 vehicle detection\yolov4.weights")
net.setInputSize(608,608)
net.setInputScale(1.0/255)
net.setInputSwapRB(True)
# frame=cv2.imread(r"download.jpg")

with open('D:\gil\demo\yolov4 vehicle detection\obj.names','rt') as f:
    names=f.read().rstrip('\n').split('\n')
fpsLimit = 1 # throttle limit
startTime = time.time()
cap = cv2.VideoCapture("b.dav")
@sio.event
def connect():
    while True:
            ret,frame = cap.read()
        # print(type(frame))
        # frame=cv2.imread('download.jpg')
        # nowTime = time.time()
        # if (int(nowTime - startTime)) > fpsLimit:
            classes,confidances,boxes=net.detect(frame,confThreshold=0.1,nmsThreshold=0.4)
            if type(classes)==type((1,1)):
                continue
            # print(classes)
            # print(results)
            results=[]
            print(results)
            time.sleep(5)
            for classId,confidance,box in zip(classes.flatten(),confidances.flatten(),boxes):
                label='%.2f' % confidance
                label = '%s: %s' % (names[classId],label)
                # print(label)
                labelSize,baseLine= cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,0.5,1)
                left,top,wedth,height=box
                top=max(top,labelSize[1])
                # cv2.rectangle(frame,box,color=(0,255,0),thickness=3)
                # cv2.rectangle(frame,(left,top-labelSize[1]),(left+labelSize[0],top +baseLine),(255,255,255),cv2.FILLED)
                # cv2.putText(frame,label,(left,top),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
                # startTime = time.time() # reset time
                results.append({
                    "label":str(names[classId]),
                    "prob":str('%.2f' % confidance),
                    "x":str(left),
                    "y":str(top),
                    "w":str(wedth),
                    "h":str(height)
                })
            # ret,buffer=cv2.imencode(".jpg",frame)
            # buffer=buffer.tobytes()
            # print(buffer)
            # print(results)
            # print("len of list :",len(results))
            frame = base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()

            # string_img = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
            # tag=str(random.random()*100)
            
            # print("result",results)
            dic={
                "cartotal":0,
                "bustotal":0,
                "trucktotal":0,
                "rickshawtotal":0,
                "biketotal":0,
                "vantotal":0,
                "total":0

            }
            for i in results:
                # print(i["label"])
                if i["label"] =='Motorcycle' or i["label"]=="Bicycle":
                    dic['biketotal']+=1
                    dic['total']+=1
                elif i['label']=='Auto_rikshaw':
                    dic['rickshawtotal']+=1
                    dic['total']+=1
                elif i['label']=='Bus':
                    dic['bustotal']+=1
                    dic['total']+=1
                elif i['label']=='Truck':
                    dic['trucktotal']+=1
                    dic['total']+=1
                elif i['label']=='Van':
                    dic['vantotal']+=1
                    dic['total']+=1
                else:
                    dic['cartotal']+=1
                    dic['total']+=1
            obj={
                "image":frame,
                # "tag":tag,
                "datetime":datetime.datetime.now().__str__(),
                "camera_id":"12345",
                "camera_loc":"UOB",
                "results":results,
                "counts":dic
            }

            # obj['counts']=json.dumps(dic)
            # print(obj)


            sio.emit('main page socket',obj)





        
        # print(obj)
        # cv2.imshow("frame",frame)
        # response_res=requests.post("http://127.0.0.1:5000/upload",json=obj)
        # response_res=requests.post("http://143.110.179.46:80/upload",json=obj) #home desktop
        # print(json.loads(response_res.text))
        # break
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
# cap.release()
cv2.destroyAllWindows()
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:8000')
# sio.connect('http://143.110.179.46:4444')
sio.wait()