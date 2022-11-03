from fastapi import FastAPI, File, UploadFile
from enum import Enum
import os

app = FastAPI()

FILES_PATH = "files/"
GENERIC_DIRECTORY = "all/"

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

@app.post("/sendFileTo/")
async def create_upload_file(file : UploadFile):
    outfile = open(FILES_PATH + GENERIC_DIRECTORY + file.filename, "wb+")
    a = file.file.read()
    outfile.write(a)
    outfile.close()
    return {"filename" : file.filename}

@app.post("/sendFileTo/{usr}")
async def create_upload_file(usr : ProfileName, file : UploadFile):
    outfile = open(FILES_PATH + usr + "/" + file.filename, "wb+")
    a = file.file.read()
    outfile.write(a)
    outfile.close()
    return {"filename" : file.filename, "usr":usr}

def retrieve_files_from_usr(usr:ProfileName):
    return [FILES_PATH + usr + "/" + i for i in os.listdir(FILES_PATH + usr + "/")]

def retrieve_generic_files():
    return [FILES_PATH + GENERIC_DIRECTORY + i for i in os.listdir(FILES_PATH + GENERIC_DIRECTORY)]

def sort_by_modification_date(files):
    return sorted(files, key=lambda t: -os.stat(t).st_mtime)


@app.get("/retrieveFiles/{usr}")
async def retrieve_files(usr : ProfileName):
    files = sort_by_modification_date(retrieve_files_from_usr(usr) + retrieve_generic_files())
    if len(files) > 0:
        return {"filename":files[0]}
    else:
        return {"message": "no files found"}

@app.get("/clean/")
async def clean_all():
    folders = [i.value for i in ProfileName] + [GENERIC_DIRECTORY[:-1]]
    for f in folders:
        SEARCH_PATH = FILES_PATH + f + "/"
        for file in os.listdir(SEARCH_PATH):
            os.remove(SEARCH_PATH + file)
    return {"message" : "ok"}