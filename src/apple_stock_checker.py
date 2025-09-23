import os
import json
import logging
import requests

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

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
        logger.error("API_BASE_URL and USER_AGENT environment variables must be set.")
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

                logger.debug("--- Raw API Response for model %s ---", model)
                logger.debug(json.dumps(data, indent=2, ensure_ascii=False))

                stores = data.get("body", {}).get("PickupMessage", {}).get("stores", [])
                
                available_stores_for_model = []
                for store in stores:
                    store_name = store.get("storeName")
                    parts_availability = store.get("partsAvailability", {})
                    
                    for part_number, details in parts_availability.items():
                        # If any part is available, we consider the model to be in stock.
                        if details.get("pickupDisplay") == "available":
                            if store_name:
                                available_stores_for_model.append(store_name)
                
                current_stock[model] = sorted(list(set(available_stores_for_model)))

            except requests.exceptions.RequestException as e:
                logger.warning("Error checking stock for model %s: Network issue. (%s)", model, e)
                continue
            except json.JSONDecodeError:
                logger.warning("Error checking stock for model %s: Failed to decode JSON response.", model)
                continue

    return current_stock
