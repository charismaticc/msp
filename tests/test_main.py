import requests

api_url = "http://localhost:8000"


def test_healthcheck():
    response = requests.get(f"{api_url}/__health")
    assert response.status_code == 200


class TestPhones:
    def test_get_empty_phones(self):
        response = requests.get(f"{api_url}/v1/phones")
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_phones(self):
        body = {'model': "Model", "developer": "developer"}
        response = requests.post(f"{api_url}/v1/phones", json=body)
        assert response.status_code == 200
        assert response.json().get('model') == 'Model'
        assert response.json().get('developer') == 'Developer'
        assert response.json().get('id') == 0

    def test_get_phones_by_id(self):
        response = requests.get(f"{api_url}/v1/phones/0")
        assert response.status_code == 200
        assert response.json().get('model') == 'Model'
        assert response.json().get('developer') == 'Developer'
        assert response.json().get('id') == 0

    def test_get_empty_phones(self):
        response = requests.get(f"{api_url}/v1/phones")
        assert response.status_code == 200
        assert len(response.json()) == 1