from fastapi import FastAPI
from enum import Enum
import os

app = FastAPI()

MESSAGE_PATH = "messages/"

NO_MESSAGE_FOUND = "No message found"

class ProfileName(str, Enum):
    profileA = "red"
    profileB = "blue"
    profileC = "green"
    profileD = "yellow"
    profileE = "purple"
    profileF = "black"
    profileG = "white"
    profileH = "brown"
    profileI = "orange"

@app.get("/")
def hello():
    return {"message":"Hello!"}

@app.post("/sendMessageTo")
async def create_upload_file(msg : str, sender : ProfileName):
    for usr in [i.value for i in ProfileName]:
        if usr == sender:continue
        outfile = open(MESSAGE_PATH + usr, "a+")
        outfile.write(msg + "\n")
        outfile.close()
    return {"status" : "ok", "usr":"all"}


@app.post("/sendMessageTo/{usr}")
async def create_upload_file(usr : ProfileName, msg : str, sender : str):
    outfile = open(MESSAGE_PATH + usr, "a+")
    outfile.write(msg + "\n")
    outfile.close()
    return {"status" : "ok", "usr":usr}


@app.get("/retrieveMessages/{usr}")
async def retrieve_messages(usr : ProfileName):
    if usr not in os.listdir(MESSAGE_PATH):
        return {"message": NO_MESSAGE_FOUND}
    inFile = open(MESSAGE_PATH + usr, "r+")
    inFile = inFile.readlines()
    if len(inFile) > 0:
        msg = inFile[0].strip()
        inFile = inFile[1:]
        outFile = open(MESSAGE_PATH + usr, "w+")
        for i in inFile:
            outFile.write(i)
        outFile.close()
        return {"message":msg}
    else:
        return {"message": NO_MESSAGE_FOUND}

@app.get("/cleanMessages/")
async def clean_all():
    SEARCH_PATH = MESSAGE_PATH
    for file in os.listdir(SEARCH_PATH):
        os.remove(SEARCH_PATH + file)
    return {"message" : "ok"}