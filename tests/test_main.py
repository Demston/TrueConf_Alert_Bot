import pytest
from fastapi.testclient import TestClient
from main_app import app

client = TestClient(app)


@pytest.fixture
def grafana_payload():
    return {
        "title": "Critical Erros",
        "state": "alerting",
        "message": "Metric Value: 5"
    }


def test_grafana_webhook_success(grafana_payload):
    """Check API work / Проверяем работу API"""
    response = client.post("/webhook/grafana", json=grafana_payload)
    assert response.status_code == 200


def test_webhook_invalid_json(grafana_payload):
    """Send JSON / Отправляем JSON"""
    response = client.post("/webhook/grafana", json=grafana_payload)
    assert response.status_code != 500
