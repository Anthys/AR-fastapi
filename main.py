from typing import Union
from fastapi import FastAPI
import os
from utilities import ProfileName, Message, OPEN_PROFILE
import json
from datetime import datetime, timedelta

app = FastAPI()

timeConstraint = True

JSON_MAIN = "message"

MESSAGE_PATH = "messages/"

NO_MESSAGE_FOUND = "No message found"

StrNone = Union[str, None]

@app.get("/")
def hello():
    return {JSON_MAIN:"Hello!"}

@app.get("/profiles")
def getProfiles():
    out = [i.value for i in ProfileName]
    return {JSON_MAIN:out}

@app.post("/sendMessageTo")
async def send_message_to_everyone(msg : str, sender : ProfileName, openableBy : StrNone= None):
    for usr in [i.value for i in ProfileName]:
        if usr == sender:continue
        message = Message(msg, openableBy, sender, usr)
        outfile = open(MESSAGE_PATH + usr, "a+")
        outfile.write(json.dumps(message.__dict__, default=str) + "\n")
        outfile.close()
    return {"status" : "ok", "usr":"all"}


@app.post("/sendMessageTo/{usr}")
async def send_message_to_usr(usr : ProfileName, msg : str, sender : StrNone = None, openableBy : StrNone= None):
    message = Message(msg, openableBy, sender, usr)
    outfile = open(MESSAGE_PATH + usr, "a+")
    outfile.write(json.dumps(message.__dict__, default=str) + "\n")
    outfile.close()
    return {"status" : "ok", "usr":usr}


@app.get("/retrieveMessages/{usr}")
async def retrieve_messages(usr : ProfileName):
    return retrieve_message(usr)

def retrieve_message(usr : ProfileName):
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
        msg = json.loads(msg)
        now = datetime.now()
        msgTime = datetime.strptime(msg["time"], '%Y-%m-%d %H:%M:%S.%f')
        delta = timedelta(seconds=8)
        if (timeConstraint and now-delta>msgTime):
            return retrieve_message(usr)
        return {JSON_MAIN:msg}
    else:
        return {JSON_MAIN: NO_MESSAGE_FOUND}

@app.get("/cleanMessages/")
async def clean_all():
    SEARCH_PATH = MESSAGE_PATH
    for file in os.listdir(SEARCH_PATH):
        os.remove(SEARCH_PATH + file)
    return {JSON_MAIN : "ok"}