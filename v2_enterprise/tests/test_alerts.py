import unittest
from datetime import datetime


# test for checking logic of create message
def format_alert_message(alert_data: dict) -> str:
    """Filter Check"""
    timestamp = datetime.now().strftime('%H:%M')
    alerts = alert_data.get('alerts', [])
    full_message = ''

    for alert in alerts:
        values = alert.get('values') or {}
        val = values.get('B', values.get('A', 0))
        if val == 0:
            continue
        alert_name = alert.get('labels', {}).get('alertname', 'Алерт')
        full_message = f"{timestamp} {alert_name}: {val}"

    return full_message


class TestGrafanaAlerts(unittest.TestCase):
    def test_successful_alert_processing(self):
        """Test. Creating message if value > 0"""
        mock_payload = {
            "alerts": [{"labels": {"alertname": "Тестовый Алерт"}, "values": {"A": 5}}]
        }
        result = format_alert_message(mock_payload)
        self.assertTrue(len(result) > 0)
        self.assertIn("Тестовый Алерт: 5", result)

    def test_phantom_alert_ignored(self):
        """Test. If value = 0, message must be empty"""
        mock_payload = {
            "alerts": [{"labels": {"alertname": "Пустой Алерт"}, "values": {"A": 0}}]
        }
        result = format_alert_message(mock_payload)
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
