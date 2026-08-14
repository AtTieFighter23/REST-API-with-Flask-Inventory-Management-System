from flask import Flask, jsonify, request

from data import inventory

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """Return a welcome message."""
    return jsonify({"message": "Welcome to the Inventory Management API"}), 200


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Return all inventory items."""
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """Return a single inventory item by id, or 404 if not found."""
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"error": f"Item with id {item_id} not found"}), 404


@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    """Create a new inventory item from JSON input."""
    data = request.get_json()

    if not data or "product_name" not in data:
        return jsonify({"error": "Missing required field: product_name"}), 400

    price = data.get("price", 0.0)
    stock = data.get("stock", 0)

    if not isinstance(price, (int, float)) or not isinstance(stock, int):
        return jsonify({"error": "price must be a number and stock must be an integer"}), 400

    new_id = max((item["id"] for item in inventory), default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": price,
        "stock": stock,
    }
    inventory.append(new_item)

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    """Update an existing inventory item's fields."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No update data provided"}), 400

    if "price" in data and not isinstance(data["price"], (int, float)):
        return jsonify({"error": "price must be a number"}), 400

    if "stock" in data and not isinstance(data["stock"], int):
        return jsonify({"error": "stock must be an integer"}), 400

    for item in inventory:
        if item["id"] == item_id:
            for field in ("product_name", "brands", "ingredients_text", "price", "stock"):
                if field in data:
                    item[field] = data[field]
            return jsonify(item), 200

    return jsonify({"error": f"Item with id {item_id} not found"}), 404


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    """Remove an inventory item by id."""
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return "", 204

    return jsonify({"error": f"Item with id {item_id} not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)