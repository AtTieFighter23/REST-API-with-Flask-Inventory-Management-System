import pytest

from app import app
from data import inventory


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset the in-memory inventory before each test."""
    inventory.clear()
    inventory.append({
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 4.99,
        "stock": 25,
    })
    inventory.append({
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Dave's Killer Bread",
        "ingredients_text": "Whole wheat flour, water, yeast, honey",
        "price": 5.49,
        "stock": 12,
    })


@pytest.fixture
def client():
    return app.test_client()


def test_welcome_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_single_inventory_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["product_name"] == "Organic Almond Milk"


def test_get_single_inventory_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_create_inventory_item(client):
    payload = {"product_name": "Test Product", "price": 9.99, "stock": 10}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"
    assert "id" in data


def test_create_inventory_item_missing_name(client):
    response = client.post("/inventory", json={"price": 9.99})
    assert response.status_code == 400


def test_update_inventory_item(client):
    response = client.patch("/inventory/1", json={"price": 6.99, "stock": 50})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 6.99
    assert data["stock"] == 50


def test_update_inventory_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1.00})
    assert response.status_code == 404


def test_delete_inventory_item(client):
    response = client.delete("/inventory/2")
    assert response.status_code == 204

    follow_up = client.get("/inventory/2")
    assert follow_up.status_code == 404


def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404