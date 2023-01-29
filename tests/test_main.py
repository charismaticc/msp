import requests

api_url = "http://localhost:8000"


def test_healthcheck():
    response = requests.get(f"{api_url}/__health")
    assert response.status_code == 200
