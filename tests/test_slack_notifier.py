import pytest
from unittest.mock import patch, MagicMock
from slack_sdk.errors import SlackApiError
from src.slack_notifier import send_notification

@patch('src.slack_notifier.WebhookClient')
@patch('src.slack_notifier.os.environ.get')
def test_send_notification_success(mock_os_get, mock_webhook_client):
    """
    Tests a successful notification send.
    """
    # Mock the environment variable
    mock_os_get.return_value = "https://hooks.slack.com/services/FAKE/URL"
    
    # Mock the WebhookClient instance and its send() method
    mock_instance = MagicMock()
    # Simulate a successful response from the Slack API
    mock_instance.send.return_value.status_code = 200
    mock_webhook_client.return_value = mock_instance

    result = send_notification("Test message")

    assert result is True
    mock_os_get.assert_called_once_with("SLACK_WEBHOOK_URL")
    mock_webhook_client.assert_called_once_with("https://hooks.slack.com/services/FAKE/URL")
    mock_instance.send.assert_called_once_with(text="Test message")

@patch('src.slack_notifier.os.environ.get')
def test_send_notification_missing_env_var(mock_os_get):
    """
    Tests that the function returns False if the environment variable is not set.
    """
    # Simulate the environment variable being absent
    mock_os_get.return_value = None

    result = send_notification("Test message")

    assert result is False
    mock_os_get.assert_called_once_with("SLACK_WEBHOOK_URL")

@patch('src.slack_notifier.WebhookClient')
@patch('src.slack_notifier.os.environ.get')
def test_send_notification_api_error(mock_os_get, mock_webhook_client):
    """
    Tests the function's behavior when a SlackApiError is raised.
    """
    mock_os_get.return_value = "https://hooks.slack.com/services/FAKE/URL"
    
    # Configure the mock to raise a SlackApiError, simulating an API issue
    mock_instance = MagicMock()
    mock_instance.send.side_effect = SlackApiError("API Error", {"ok": False, "error": "invalid_auth"})
    mock_webhook_client.return_value = mock_instance

    result = send_notification("Test message")

    assert result is False

@patch('src.slack_notifier.WebhookClient')
@patch('src.slack_notifier.os.environ.get')
def test_send_notification_http_error(mock_os_get, mock_webhook_client):
    """
    Tests the function's behavior on a non-200 HTTP status code response.
    """
    mock_os_get.return_value = "https://hooks.slack.com/services/FAKE/URL"
    
    # Simulate a response object with a non-200 status code
    mock_instance = MagicMock()
    mock_instance.send.return_value.status_code = 404
    mock_instance.send.return_value.body = "Not Found"
    mock_webhook_client.return_value = mock_instance

    result = send_notification("Test message")

    assert result is False
