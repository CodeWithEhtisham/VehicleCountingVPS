# # counterFlag=None
# import json
# def readJson():
#     with open("utils.json",'r') as file:
#         data=json.load(file)
#         file.close()
#     return data
#     # pass
# def writeJson(value):
#     data=readJson()
#     with open("utils.json",'w') as file:
#         print(data)
#         data["counterFlag"]=value
#         print("update json",data)
#         json.dump(data,file)
#         file.close()
# def setter(flag):
#     writeJson(flag)
# def getter():
#     data=readJson()
#     return data["counterFlag"]


counterFlag=True
def setter(value):
    global counterFlag
    counterFlag=value
def getter():
    global counterFlag
    return counterFlag