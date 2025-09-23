import os
import sys
import logging
from src import state_manager, apple_stock_checker, slack_notifier

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_notification_message(old_state: dict, new_state: dict) -> str:
    """
    Compares the old and new stock states and creates a human-readable
    notification message for any changes.
    """
    messages = []
    all_models = set(old_state.keys()) | set(new_state.keys())

    for model in sorted(list(all_models)):
        old_stores = set(old_state.get(model, []))
        new_stores = set(new_state.get(model, []))

        if old_stores == new_stores:
            continue

        added_stores = new_stores - old_stores
        removed_stores = old_stores - new_stores

        if added_stores:
            messages.append(f"✅ Stock added for {model} at: {', '.join(sorted(list(added_stores)))}")
        if removed_stores:
            messages.append(f"❌ Stock removed for {model} at: { ', '.join(sorted(list(removed_stores)))}")
            
    return "\n".join(messages)

def main():
    """
    Main function to orchestrate the stock checking process.
    """
    product_models_str = os.environ.get("PRODUCT_MODELS")
    location = os.environ.get("LOCATION")

    if not product_models_str or not location:
        logger.critical("PRODUCT_MODELS and LOCATION environment variables must be set.")
        sys.exit(1)
    
    product_models = [model.strip() for model in product_models_str.split(',')]

    old_state = state_manager.read_state()

    logger.info("Checking stock for models: %s at location: %s", product_models, location)
    new_state = apple_stock_checker.check_stock(product_models, location)
    logger.info("Current stock status: %s", new_state)

    state_manager.write_state(new_state)
    logger.info("Successfully updated state file.")

    message = create_notification_message(old_state, new_state)

    if message:
        logger.info("Changes detected. Sending notification...\n%s", message)
        success = slack_notifier.send_notification(message)
        if success:
            logger.info("Slack notification sent successfully.")
        else:
            logger.error("Failed to send Slack notification.")
    else:
        logger.info("No stock changes detected.")

if __name__ == "__main__":
    main()