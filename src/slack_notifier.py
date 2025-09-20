import os
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError

def send_notification(message: str) -> bool:
    """
    Sends a message to a Slack channel using an incoming webhook URL.

    The webhook URL is read from the SLACK_WEBHOOK_URL environment variable.
    This function includes error handling for missing environment variables
    and issues with the Slack API call.

    Args:
        message (str): The text message to be sent to Slack.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Error: SLACK_WEBHOOK_URL environment variable not set.")
        return False

    webhook = WebhookClient(webhook_url)
    
    try:
        response = webhook.send(text=message)
        
        if response.status_code == 200:
            return True
        else:
            # Handle non-200 responses that aren't SlackApiErrors
            print(f"Error sending Slack notification: Received status code {response.status_code}")
            print(f"Response body: {response.body}")
            return False
            
    except SlackApiError as e:
        # Handle specific Slack API errors (e.g., invalid URL, bad payload)
        print(f"Error sending Slack notification: {e.response['error']}")
        return False
    except Exception as e:
        # Handle other potential exceptions (e.g., network issues)
        print(f"An unexpected error occurred while sending Slack notification: {e}")
        return False
