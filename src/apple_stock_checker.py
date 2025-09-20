import requests
import json

# Base URL for the pickup recommendations API.
# Location and product will be added as query parameters.
BASE_URL = "https://www.apple.com/jp/shop/pickup-message-recommendations?mts.0=regular&cppart=UNLOCKED_JP"

def check_stock(models: list, location: str) -> dict:
    """
    Checks in-store pickup availability for a list of product models.

    Args:
        models (list): A list of product model strings to check.
        location (str): The location (e.g., a postal code) to check against.

    Returns:
        dict: A dictionary where keys are product models and values are a list
              of store names where the product is available. If a model check
              fails due to an error, its value will be an empty list.
    """
    # Initialize a dictionary to hold the stock status for all models.
    current_stock = {model: [] for model in models}
    
    with requests.Session() as session:
        # Use a common browser User-Agent to avoid being blocked.
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        for model in models:
            url = f"{BASE_URL}&location={location}&product={model}"
            
            try:
                response = session.get(url)
                # Raise an HTTPError for bad responses (4xx or 5xx)
                response.raise_for_status()
                data = response.json()

                stores = data.get("body", {}).get("PickupMessage", {}).get("stores", [])
                
                available_stores_for_model = []
                for store in stores:
                    store_name = store.get("storeName")
                    parts_availability = store.get("partsAvailability", {})
                    
                    # Iterate through parts in case the response key is different
                    for part_number, details in parts_availability.items():
                        # Check if it's the correct model and is available
                        if part_number == model and details.get("pickupDisplay") == "available":
                            if store_name:
                                available_stores_for_model.append(store_name)
                
                # Use set to store unique store names, then sort for consistent output
                current_stock[model] = sorted(list(set(available_stores_for_model)))

            except requests.exceptions.RequestException as e:
                print(f"Error checking stock for model {model}: Network issue. ({e})")
                # On a network error for one model, we simply leave its stock list empty
                # and continue to the next model to ensure resilience.
                continue
            except json.JSONDecodeError:
                print(f"Error checking stock for model {model}: Failed to decode JSON response.")
                # Also continue to the next model if one response is bad.
                continue

    return current_stock
