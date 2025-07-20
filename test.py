import pytest
from fastapi.testclient import TestClient
from main import app  # FastAPI app'inin tanımlandığı dosya

client = TestClient(app)

def test_create_clan():
    payload = {
        "name": "TestClan",
        "region": "TR"
    }
    response = client.post("/clans", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert data["message"] == "Clan created successfully."
    assert "id" in data

def test_create_existing_clan():
    payload = {
        "name": "TestClan",
        "region": "TR"
    }
    # Aynı ismi tekrar yaratmayı dene
    response = client.post("/clans", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Clan already exists."

def test_delete_clan():
    # Önce clan oluştur
    payload = {
        "name": "ClanToDelete",
        "region": "US"
    }
    create_resp = client.post("/clans", json=payload)
    clan_id = create_resp.json()["id"]

    # Şimdi sil
    del_resp = client.delete(f"/clans/{clan_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Clan deleted successfully."
    assert del_resp.json()["id"] is None

def test_delete_nonexistent_clan():
    fake_id = "123e4567-e89b-12d3-a456-426614174000"  # UUID formatında sahte id
    response = client.delete(f"/clans/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Clan deletion failed: clan doesn't exist."
