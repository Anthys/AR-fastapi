from typing import Union
from fastapi import FastAPI
import os
from utilities import ProfileName, Message, OPEN_PROFILE
import json
from datetime import datetime, timedelta

app = FastAPI()

timeConstraint = True

JSON_MAIN = "out"

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

@app.get("/verifyProfile/{usr}")
def verifyProfile(usr : str):
    bol = usr in [i.value for i in ProfileName]
    return {JSON_MAIN: str(bol)}

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
async def retrieve_messages(usr : ProfileName, requester : StrNone = None):
    if usr not in os.listdir(MESSAGE_PATH):
        return {JSON_MAIN: NO_MESSAGE_FOUND}
    inFile = open(MESSAGE_PATH + usr, "r+")
    inFile = inFile.readlines()
    msg = "DEFAULT MESSAGE NOT OVERRIDEN"
    lineIndex, inFile, isSuitable, isEOF = is_suitable(0, inFile, requester)
    while not isEOF:
        if isSuitable:
            msg = inFile[lineIndex].strip()
            msg = json.loads(msg)
            inFile = inFile[:lineIndex] + inFile[lineIndex+1:]
            break
        lineIndex, inFile, isSuitable, isEOF = is_suitable(lineIndex, inFile, requester)

    outFile = open(MESSAGE_PATH + usr, "w+")
    for i in inFile:
        outFile.write(i)
    outFile.close()

    if isSuitable:
        return {JSON_MAIN:msg}
    else:
        return {JSON_MAIN: NO_MESSAGE_FOUND}

def is_suitable(index, inFile, requester):
    if (len(inFile)<=index):
        # A: NO MORE LINES, BREAK
        return index, inFile, False, True
    msg = inFile[index].strip()
    if (msg == ""): 
        # A: NO MORE LINES, BREAK
        return index+1, inFile, False, True
    msg = json.loads(msg)
    now = datetime.now()
    msgTime = datetime.strptime(msg["time"], '%Y-%m-%d %H:%M:%S.%f')
    delta = timedelta(seconds=8)
    if (timeConstraint and now-delta>msgTime):
        # B: LINE IS OUTDATED, IT IS REMOVED
        return index, inFile[:index] + inFile[index+1:], False, False
    if (msg["openableBy"] != None and requester != msg["openableBy"]):
        # C : REQUESTER DOESN4T HAVE ACCESS, NEXT LINE
        return index+1, inFile, False, False
    # D : SUITABLE
    return index, inFile, True, False

@app.get("/cleanMessages/")
async def clean_all():
    SEARCH_PATH = MESSAGE_PATH
    for file in os.listdir(SEARCH_PATH):
        os.remove(SEARCH_PATH + file)
    return {JSON_MAIN : "ok"}