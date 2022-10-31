from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello!"}

@app.post("/uploadfile/")
async def create_upload_file(file : UploadFile):
    outfile = open("files/" + file.filename, "wb+")
    a = file.file.read()
    outfile.write(a)
    outfile.close()
    return {"filename" : file.filename}