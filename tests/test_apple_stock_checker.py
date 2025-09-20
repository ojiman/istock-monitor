import json
import pytest
import requests
from unittest.mock import MagicMock, patch
from src.apple_stock_checker import check_stock

# A simplified version of the user-provided sample JSON response
SAMPLE_API_RESPONSE = {
  "body": {
    "PickupMessage": {
      "stores": [
        {
          "storeName": "渋谷",
          "partsAvailability": {
            "MG6A4J/A": {"pickupDisplay": "available"}
          }
        },
        {
          "storeName": "新宿",
          "partsAvailability": {
            "MG6A4J/A": {"pickupDisplay": "available"},
            "MG6C4J/A": {"pickupDisplay": "unavailable"}
          }
        }
      ]
    }
  }
}

# A sample response where no stores have the part
NO_STOCK_RESPONSE = {
    "body": {
        "PickupMessage": {
            "stores": [
                {"storeName": "渋谷", "partsAvailability": {}},
                {"storeName": "新宿", "partsAvailability": {}}
            ]
        }
    }
}

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_success(mock_get):
    """
    Tests a successful stock check where products are available.
    """
    # Configure the mock to return a successful response with JSON data
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = SAMPLE_API_RESPONSE
    mock_get.return_value = mock_response

    models_to_check = ["MG6A4J/A", "MG6C4J/A"]
    location = "123-4567"
    
    result = check_stock(models_to_check, location)

    # Assertions
    assert "MG6A4J/A" in result
    assert "MG6C4J/A" in result
    # Should find MG6A4J/A in two stores, sorted alphabetically
    assert result["MG6A4J/A"] == ["新宿", "渋谷"]
    # Should find MG6C4J/A is unavailable
    assert result["MG6C4J/A"] == []
    # Verify the mock was called for each model
    assert mock_get.call_count == len(models_to_check)

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_no_stock(mock_get):
    """
    Tests a successful API call where no stock is available for the model.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = NO_STOCK_RESPONSE
    mock_get.return_value = mock_response

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_network_error(mock_get):
    """
    Tests the function's behavior during a network error.
    """
    # Configure the mock to raise a RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Network Error")

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    # The function should handle the error and return a dict with an empty list
    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_bad_json(mock_get):
    """
    Tests the function's behavior when the API returns non-JSON content.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    # Configure the mock to raise a JSONDecodeError when .json() is called
    mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
    mock_get.return_value = mock_response

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    # The function should handle the error and return a dict with an empty list
    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1
