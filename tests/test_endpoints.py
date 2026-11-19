import pytest 
from fastapi.testclient import TestClient
from app.main import app 
from pathlib import Path

# init test client 
client = TestClient(app)

def test_get_homepage():
    """Client GET request fetches homepage markdown."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<title>URL Shortener</title>" in response.text

@pytest.mark.parametrize(
    "method", 
    ["POST", "PUT", "PATCH", "DELETE", "QUERY", "HEAD", "OPTIONS", "TRACE", "CONNECT"]
)
def test_other_method_homepage(method):
    """Client non-GET requests raises error."""
    response = client.request(method, "/")
    assert response.status_code == 405 

