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
            "MG6A4J/A": {"pickupDisplay": "available"}
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
def test_check_stock_success(mock_get, monkeypatch):
    """
    Tests a successful stock check where products are available.
    """
    monkeypatch.setenv("API_BASE_URL", "https://fake.apple.com")
    monkeypatch.setenv("USER_AGENT", "Test Agent")

    # Create separate mock responses for each API call
    mock_response_stock = MagicMock()
    mock_response_stock.raise_for_status.return_value = None
    mock_response_stock.json.return_value = SAMPLE_API_RESPONSE

    mock_response_no_stock = MagicMock()
    mock_response_no_stock.raise_for_status.return_value = None
    mock_response_no_stock.json.return_value = NO_STOCK_RESPONSE

    # Use side_effect to return different responses for each call
    mock_get.side_effect = [mock_response_stock, mock_response_no_stock]

    models_to_check = ["MG6A4J/A", "MG6C4J/A"]
    location = "123-4567"
    
    result = check_stock(models_to_check, location)

    # Assertions
    assert "MG6A4J/A" in result
    assert "MG6C4J/A" in result
    assert result["MG6A4J/A"] == ["新宿", "渋谷"]
    assert result["MG6C4J/A"] == []
    assert mock_get.call_count == len(models_to_check)

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_no_stock(mock_get, monkeypatch):
    """
    Tests a successful API call where no stock is available for the model.
    """
    monkeypatch.setenv("API_BASE_URL", "https://fake.apple.com")
    monkeypatch.setenv("USER_AGENT", "Test Agent")

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = NO_STOCK_RESPONSE
    mock_get.return_value = mock_response

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_network_error(mock_get, monkeypatch):
    """
    Tests the function's behavior during a network error.
    """
    monkeypatch.setenv("API_BASE_URL", "https://fake.apple.com")
    monkeypatch.setenv("USER_AGENT", "Test Agent")

    mock_get.side_effect = requests.exceptions.RequestException("Network Error")

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1

@patch('src.apple_stock_checker.requests.Session.get')
def test_check_stock_bad_json(mock_get, monkeypatch):
    """
    Tests the function's behavior when the API returns non-JSON content.
    """
    monkeypatch.setenv("API_BASE_URL", "https://fake.apple.com")
    monkeypatch.setenv("USER_AGENT", "Test Agent")

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
    mock_get.return_value = mock_response

    models_to_check = ["MG6A4J/A"]
    result = check_stock(models_to_check, "123-4567")

    assert result["MG6A4J/A"] == []
    assert mock_get.call_count == 1
