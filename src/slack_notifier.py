import os
import logging
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

def send_notification(message: str) -> bool:
    """
    Sends a message to a Slack channel using an incoming webhook URL.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logger.error("SLACK_WEBHOOK_URL environment variable not set.")
        return False

    webhook = WebhookClient(webhook_url)
    
    try:
        response = webhook.send(text=message)
        
        if response.status_code == 200:
            return True
        else:
            logger.error("Error sending Slack notification: Received status code %s", response.status_code)
            logger.error("Response body: %s", response.body)
            return False
            
    except SlackApiError as e:
        logger.error("Error sending Slack notification: %s", e.response['error'])
        return False
    except Exception as e:
        logger.error("An unexpected error occurred while sending Slack notification: %s", e)
        return False