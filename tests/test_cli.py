from unittest.mock import patch, Mock

import cli


@patch("cli.requests.get")
def test_view_all_items_success(mock_get, capsys):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {"id": 1, "product_name": "Almond Milk", "brands": "Silk",
         "ingredients_text": "", "price": 4.99, "stock": 25}
    ]
    mock_get.return_value = mock_response

    cli.view_all_items()

    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("cli.requests.get")
def test_view_all_items_empty(mock_get, capsys):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    cli.view_all_items()

    captured = capsys.readouterr()
    assert "Inventory is empty." in captured.out


@patch("cli.requests.get")
def test_view_all_items_api_unreachable(mock_get, capsys):
    import requests
    mock_get.side_effect = requests.RequestException("connection refused")

    cli.view_all_items()

    captured = capsys.readouterr()
    assert "Error" in captured.out


@patch("cli.requests.post")
@patch("builtins.input", side_effect=["New Item", "TestBrand", "5.00", "10"])
def test_add_item_success(mock_input, mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 3, "product_name": "New Item", "brands": "TestBrand",
        "ingredients_text": "", "price": 5.00, "stock": 10
    }
    mock_post.return_value = mock_response

    cli.add_item()

    captured = capsys.readouterr()
    assert "Item added successfully" in captured.out


@patch("builtins.input", side_effect=[""])
def test_add_item_missing_name(mock_input, capsys):
    cli.add_item()

    captured = capsys.readouterr()
    assert "product name is required" in captured.out


@patch("cli.requests.delete")
@patch("builtins.input", side_effect=["1"])
def test_delete_item_success(mock_input, mock_delete, capsys):
    mock_response = Mock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    cli.delete_item()

    captured = capsys.readouterr()
    assert "deleted successfully" in captured.out


@patch("builtins.input", side_effect=["abc"])
def test_delete_item_invalid_id(mock_input, capsys):
    cli.delete_item()

    captured = capsys.readouterr()
    assert "must be a number" in captured.out


@patch("cli.fetch_by_barcode")
@patch("builtins.input", side_effect=["b", "3017624010701", "n"])
def test_find_item_on_api_barcode_found_no_add(mock_input, mock_fetch, capsys):
    mock_fetch.return_value = {"product_name": "Nutella", "brands": "Ferrero"}

    cli.find_item_on_api()

    captured = capsys.readouterr()
    assert "Found: Nutella" in captured.out


@patch("cli.fetch_by_barcode")
@patch("builtins.input", side_effect=["b", "0000000000000"])
def test_find_item_on_api_not_found(mock_input, mock_fetch, capsys):
    mock_fetch.return_value = None

    cli.find_item_on_api()

    captured = capsys.readouterr()
    assert "No product found" in captured.out