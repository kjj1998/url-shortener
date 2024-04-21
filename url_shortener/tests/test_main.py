"""Unit tests for the main app"""

from fastapi.testclient import TestClient

from url_shortener.web.app import app

client = TestClient(app)

def test_get_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/url-shortener")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from local"}
