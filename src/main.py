import os
import sys
from src import state_manager, apple_stock_checker, slack_notifier

def create_notification_message(old_state: dict, new_state: dict) -> str:
    """
    Compares the old and new stock states and creates a human-readable
    notification message for any changes.

    Args:
        old_state (dict): The previous stock state.
        new_state (dict): The current stock state.

    Returns:
        str: A formatted string detailing the changes. Returns an empty
             string if there are no changes.
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
    # 1. Load configuration from environment variables
    product_models_str = os.environ.get("PRODUCT_MODELS")
    location = os.environ.get("LOCATION")

    if not product_models_str or not location:
        print("Error: PRODUCT_MODELS and LOCATION environment variables must be set.")
        sys.exit(1)
    
    product_models = [model.strip() for model in product_models_str.split(',')]

    # 2. Read the old state
    old_state = state_manager.read_state()

    # 3. Check for the new stock state
    print(f"Checking stock for models: {product_models} at location: {location}")
    new_state = apple_stock_checker.check_stock(product_models, location)
    print(f"Current stock status: {new_state}")

    # 4. Write the new state immediately after a successful API call
    state_manager.write_state(new_state)
    print("Successfully updated state file.")

    # 5. Compare states and create a notification message
    message = create_notification_message(old_state, new_state)

    # 6. If there are changes, send a notification
    if message:
        print(f"Changes detected. Sending notification:\n{message}")
        success = slack_notifier.send_notification(message)
        if success:
            print("Slack notification sent successfully.")
        else:
            print("Failed to send Slack notification.")
    else:
        print("No stock changes detected.")

if __name__ == "__main__":
    main()
