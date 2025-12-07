"""Integration tests"""
import pytest

def test_auth_flow(client):
    response = client.post("/auth/signup", json={"email": "test@example.com", "password": "pass", "name": "User"})
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_task_crud(client):
    response = client.post("/tasks", json={"title": "Task", "description": "Desc"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    assert client.get(f"/tasks/{task_id}").status_code == 200
    assert client.put(f"/tasks/{task_id}", json={"title": "Updated"}).status_code == 200
    assert client.delete(f"/tasks/{task_id}").status_code == 204
