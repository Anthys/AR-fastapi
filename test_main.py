from urllib import response
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_file():
    response = client.post("/uploadfile/",
    files={"file":("oui", open("oui.txt", "rb"))}
    )
    print(response.json())