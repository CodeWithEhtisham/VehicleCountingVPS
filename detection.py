import cv2
import matplotlib.pyplot as plt
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import datetime
import time
import requests
import json
import base64
import random
# im = cv2.imread(r"C:\Users\AK47\Downloads\Compressed\RealEstateManagement_C#\images (5).jpg")
# bbox, label, conf = cv.detect_common_objects(im)
# print(bbox)
# print(label)
# print(conf)
# output_image = draw_bbox(im, bbox, label, conf)
# cv2.imshow("",output_image)

# plt.show()

# define a video capture object

# frame_rate = 2
# prev = 0
# cap = cv2.VideoCapture('http://192.168.18.97:8080/video')
# plt.figure(figsize=(12,12))
# while(True):
      
#     # Capture the video frame
#     # by frame
#     time_elapsed = time.time() - prev
#     res, image = cap.read()

#     if time_elapsed > 1./frame_rate:
#         prev = time.time()
#         ret, frame = cap.read()
  
#     # Display the resulting frame
#         cv2.imshow('frame', frame)
      
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# # After the loop release the cap object
# cap.release()
# # Destroy all the windows
# cv2.destroyAllWindows()

net=cv2.dnn_DetectionModel("yolov4.cfg","yolov4.weights")
net.setInputSize(608,608)
net.setInputScale(1.0/255)
net.setInputSwapRB(True)
# frame=cv2.imread(r"download.jpg")

with open('obj.names','rt') as f:
    names=f.read().rstrip('\n').split('\n')
fpsLimit = 1 # throttle limit
startTime = time.time()
cap = cv2.VideoCapture("b.dav")
while True:
    ret,frame = cap.read()
    # print(type(frame))
    # frame=cv2.imread('download.jpg')
    nowTime = time.time()
    if (int(nowTime - startTime)) > fpsLimit:
        classes,confidances,boxes=net.detect(frame,confThreshold=0.1,nmsThreshold=0.4)
        if type(classes)==type((1,1)):
            continue
        # print(classes)
        results=[]
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
        string_img = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
        tag=str(random.random()*100)
        obj={
            "image":string_img,
            "tag":tag,
            "datetime":datetime.datetime.now().__str__(),
            "camera_id":"12345",
            "camera_loc":"UOB",
            "results":results
        }
        # print("result",results)
        # dic={
        #     "Car":0,
        #     "Bus":0,
        #     "Truck":0,
        #     "rikshaw":0,
        #     "Bike":0,
        #     "Van":0,
        #     "total":0

        # }
        # for i in results:
        #     # print(i["label"])
        #     if i["label"] =='Motorcycle' or i["label"]=="Bicycle":
        #         dic['Bike']+=1
        #         dic['total']+=1
        #     elif i['label']=='Auto_rikshaw':
        #         dic['rikshaw']+=1
        #         dic['total']+=1
        #     elif i['label']=='Bus':
        #         dic['Bus']+=1
        #         dic['total']+=1
        #     elif i['label']=='Truck':
        #         dic['Truck']+=1
        #         dic['total']+=1
        #     elif i['label']=='Van':
        #         dic['Van']+=1
        #         dic['total']+=1
        #     else:
        #         dic['Car']+=1
        #         dic['total']+=1

        # print(json.dumps(dic),tag)
        # print(obj)
        # cv2.imshow("frame",frame)
        # response_res=requests.post("http://127.0.0.1:5000/upload",json=obj)
# <<<<<<< HEAD
        response_res=requests.post("http://143.110.179.46:4000/upload",json=obj) #home desktop
# =======
        response_res=requests.post("http://192.168.18.146:5000/upload",json=obj) #home desktop
# >>>>>>> 5b8cdf8d10fbab90423e46c5fb708c5606a0cc0d
        print(json.loads(response_res.text))
        # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cap.release()
cv2.destroyAllWindows()


# cap=cv2.VideoCapture('http://192.168.18.97:8080/video')

# classes,confidances,boxes=net.detect(frame,confThreshold=0.1,nmsThreshold=0.4)
# # print(classes,confidance,boxes)
# print(len(classes.flatten()))
# for classId,confidance,box in zip(classes.flatten(),confidances.flatten(),boxes):
#     label='%.2f' % confidance
#     label = '%s: %s' % (names[classId],label)
#     print(label)
#     labelSize,baseLine= cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,0.5,1)
#     left,top,wedth,height=box
#     top=max(top,labelSize[1])
#     cv2.rectangle(frame,box,color=(0,255,0),thickness=3)
#     cv2.rectangle(frame,(left,top-labelSize[1]),(left+labelSize[0],top +baseLine),(255,255,255),cv2.FILLED)
#     cv2.putText(frame,label,(left,top),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
# plt.imshow(frame)
# plt.show()
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break