from fastapi.testclient import TestClient

from main import JSON_MAIN, NO_MESSAGE_FOUND, app

JSON_MESSAGE_STRING = "messageString"

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_clean():
    response = client.get("/cleanMessages")
    assert response.status_code == 200

def test_get_message():
    response = client.get("/retrieveMessages/blue")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN] == NO_MESSAGE_FOUND

def test_send_message1():
    response = client.post("/sendMessageTo/blue?msg=salut c'est rouge&sender=red")
    assert response.status_code == 200

def test_send_message2():
    response = client.post("/sendMessageTo/blue?msg=salut c'est rouge2&sender=red")
    assert response.status_code == 200

def test_get_message1():
    response = client.get("/retrieveMessages/blue")
    assert response.status_code == 200
    msg = response.json()[JSON_MAIN]
    assert msg[JSON_MESSAGE_STRING] == "salut c'est rouge"

def test_get_message2():
    response = client.get("/retrieveMessages/blue")
    msg = response.json()[JSON_MAIN]
    assert msg[JSON_MESSAGE_STRING] == "salut c'est rouge2"

def test_get_message3():
    response = client.get("/retrieveMessages/blue")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN] == NO_MESSAGE_FOUND


def test_send_messageGlobal():
    response = client.post("/sendMessageTo?msg=salut c'est rouge&sender=red")
    assert response.status_code == 200

def test_get_messageMultiple():
    response = client.get("/retrieveMessages/blue")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN][JSON_MESSAGE_STRING] == "salut c'est rouge"
    response = client.get("/retrieveMessages/green")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN][JSON_MESSAGE_STRING] == "salut c'est rouge"
    response = client.get("/retrieveMessages/red")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN] == NO_MESSAGE_FOUND


def test_send_message_3():
    response = client.post("/sendMessageTo/blue?msg=salut c'est rouge&sender=red&openableBy=red")
    assert response.status_code == 200

def test_get_message3_no_access():
    response = client.get("/retrieveMessages/blue?requester=blue")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN] == NO_MESSAGE_FOUND

def test_get_message3_has_access():
    response = client.get("/retrieveMessages/blue?requester=red")
    assert response.status_code == 200
    assert response.json()[JSON_MAIN][JSON_MESSAGE_STRING] == "salut c'est rouge"