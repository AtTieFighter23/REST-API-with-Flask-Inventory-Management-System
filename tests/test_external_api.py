from unittest.mock import patch, Mock

from external_api import fetch_by_barcode, fetch_by_name


@patch("external_api.requests.get")
def test_fetch_by_barcode_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero"},
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_barcode("3017624010701")

    assert result["product_name"] == "Nutella"
    mock_get.assert_called_once()


@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_barcode("0000000000000")

    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_barcode_request_fails(mock_get):
    mock_get.side_effect = Exception("network error")

    # requests.RequestException is the expected catch; simulate that instead
    import requests
    mock_get.side_effect = requests.RequestException("network error")

    result = fetch_by_barcode("3017624010701")

    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_name_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [{"product_name": "Almond Milk", "brands": "Silk"}]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_name("almond milk")

    assert result["product_name"] == "Almond Milk"


@patch("external_api.requests.get")
def test_fetch_by_name_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"products": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_name("nonexistent product xyz")

    assert result is None