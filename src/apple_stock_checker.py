import os
import json
import requests

def check_stock(models: list, location: str) -> dict:
    """
    Checks in-store pickup availability for a list of product models.

    Reads the API_BASE_URL and USER_AGENT from environment variables.

    Args:
        models (list): A list of product model strings to check.
        location (str): The location (e.g., a postal code) to check against.

    Returns:
        dict: A dictionary of stock availability.
    """
    base_url = os.environ.get("API_BASE_URL")
    user_agent = os.environ.get("USER_AGENT")

    if not base_url or not user_agent:
        print("Error: API_BASE_URL and USER_AGENT environment variables must be set.")
        # Return a structure indicating failure for all models
        return {model: [] for model in models}

    current_stock = {model: [] for model in models}
    
    with requests.Session() as session:
        session.headers.update({"User-Agent": user_agent})

        for model in models:
            url = f"{base_url}&location={location}&product={model}"
            
            try:
                response = session.get(url)
                response.raise_for_status()
                data = response.json()

                # --- Debug Log ---
                print(f"--- Raw API Response for model {model} ---")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("--- End of Raw API Response ---")

                stores = data.get("body", {}).get("PickupMessage", {}).get("stores", [])
                
                available_stores_for_model = []
                for store in stores:
                    store_name = store.get("storeName")
                    parts_availability = store.get("partsAvailability", {})
                    
                    for part_number, details in parts_availability.items():
                        if part_number == model and details.get("pickupDisplay") == "available":
                            if store_name:
                                available_stores_for_model.append(store_name)
                
                current_stock[model] = sorted(list(set(available_stores_for_model)))

            except requests.exceptions.RequestException as e:
                print(f"Error checking stock for model {model}: Network issue. ({e})")
                continue
            except json.JSONDecodeError:
                print(f"Error checking stock for model {model}: Failed to decode JSON response.")
                continue

    return current_stock