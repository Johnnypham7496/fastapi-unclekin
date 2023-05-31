from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_tc0001_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, welcome to Autobots FastAPI bootcamp"}