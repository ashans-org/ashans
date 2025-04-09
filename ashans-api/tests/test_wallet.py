from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_wallet():
    res = client.post("/wallet/create")
    assert res.status_code == 200
    assert "public_key" in res.json()