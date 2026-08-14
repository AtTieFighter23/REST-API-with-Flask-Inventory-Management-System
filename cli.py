
"""
Command-line interface for the Inventory Management System.
 
This CLI talks to the Flask API over HTTP, so the server (app.py)
must be running before using this tool.
"""
 
import requests
 
from external_api import fetch_by_barcode, fetch_by_name
 
API_URL = "http://localhost:5000"
 
 
def print_item(item):
    """Print a single inventory item in a readable format."""
    print(f"  ID: {item.get('id')}")
    print(f"  Product Name: {item.get('product_name')}")
    print(f"  Brands: {item.get('brands', '')}")
    print(f"  Ingredients: {item.get('ingredients_text', '')}")
    print(f"  Price: ${item.get('price', 0):.2f}")
    print(f"  Stock: {item.get('stock', 0)}")
 
 
def view_all_items():
    """Fetch and display all inventory items."""
    try:
        response = requests.get(f"{API_URL}/inventory", timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    items = response.json()
    if not items:
        print("Inventory is empty.")
        return
 
    for item in items:
        print_item(item)
        print("-" * 30)
 
 
def view_item_details():
    """Fetch and display a single item by id."""
    item_id = input("Enter item ID: ").strip()
    if not item_id.isdigit():
        print("Error: item ID must be a number.")
        return
 
    try:
        response = requests.get(f"{API_URL}/inventory/{item_id}", timeout=10)
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    if response.status_code == 404:
        print(f"No item found with ID {item_id}.")
        return
 
    print_item(response.json())
 
 
def add_item():
    """Prompt for details and add a new inventory item."""
    product_name = input("Product name: ").strip()
    if not product_name:
        print("Error: product name is required.")
        return
 
    brands = input("Brand (optional): ").strip()
    price_input = input("Price (optional, default 0.0): ").strip()
    stock_input = input("Stock (optional, default 0): ").strip()
 
    payload = {"product_name": product_name, "brands": brands}
 
    if price_input:
        try:
            payload["price"] = float(price_input)
        except ValueError:
            print("Error: price must be a number. Using default 0.0.")
 
    if stock_input:
        try:
            payload["stock"] = int(stock_input)
        except ValueError:
            print("Error: stock must be a whole number. Using default 0.")
 
    try:
        response = requests.post(f"{API_URL}/inventory", json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    if response.status_code == 201:
        print("Item added successfully:")
        print_item(response.json())
    else:
        print(f"Error adding item: {response.json().get('error', 'Unknown error')}")
 
 
def update_item():
    """Prompt for an item id and update its price and/or stock."""
    item_id = input("Enter item ID to update: ").strip()
    if not item_id.isdigit():
        print("Error: item ID must be a number.")
        return
 
    price_input = input("New price (leave blank to skip): ").strip()
    stock_input = input("New stock (leave blank to skip): ").strip()
 
    payload = {}
 
    if price_input:
        try:
            payload["price"] = float(price_input)
        except ValueError:
            print("Error: price must be a number. Skipping price update.")
 
    if stock_input:
        try:
            payload["stock"] = int(stock_input)
        except ValueError:
            print("Error: stock must be a whole number. Skipping stock update.")
 
    if not payload:
        print("No valid updates provided.")
        return
 
    try:
        response = requests.patch(f"{API_URL}/inventory/{item_id}", json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    if response.status_code == 200:
        print("Item updated successfully:")
        print_item(response.json())
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print(f"Error updating item: {response.json().get('error', 'Unknown error')}")
 
 
def delete_item():
    """Prompt for an item id and delete it."""
    item_id = input("Enter item ID to delete: ").strip()
    if not item_id.isdigit():
        print("Error: item ID must be a number.")
        return
 
    try:
        response = requests.delete(f"{API_URL}/inventory/{item_id}", timeout=10)
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    if response.status_code == 204:
        print(f"Item {item_id} deleted successfully.")
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print("Error deleting item.")
 
 
def find_item_on_api():
    """Search OpenFoodFacts by barcode or name, and optionally add the result to inventory."""
    choice = input("Search by (b)arcode or (n)ame? ").strip().lower()
 
    if choice == "b":
        barcode = input("Enter barcode: ").strip()
        product = fetch_by_barcode(barcode)
    elif choice == "n":
        name = input("Enter product name: ").strip()
        product = fetch_by_name(name)
    else:
        print("Error: please enter 'b' or 'n'.")
        return
 
    if product is None:
        print("No product found, or the external API is unavailable.")
        return
 
    product_name = product.get("product_name", "Unknown")
    brands = product.get("brands", "")
    ingredients_text = product.get("ingredients_text", "")
 
    print(f"Found: {product_name} ({brands})")
    add_choice = input("Add this item to inventory? (y/n): ").strip().lower()
 
    if add_choice != "y":
        return
 
    payload = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
    }
 
    try:
        response = requests.post(f"{API_URL}/inventory", json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Error: could not reach the inventory API ({e})")
        return
 
    if response.status_code == 201:
        print("Item added successfully:")
        print_item(response.json())
    else:
        print(f"Error adding item: {response.json().get('error', 'Unknown error')}")
 
 
MENU_ACTIONS = {
    "1": view_all_items,
    "2": view_item_details,
    "3": add_item,
    "4": update_item,
    "5": delete_item,
    "6": find_item_on_api,
}
 
 
def print_menu():
    print("\n--- Inventory Management CLI ---")
    print("1. View all items")
    print("2. View item details")
    print("3. Add new item")
    print("4. Update item price/stock")
    print("5. Delete item")
    print("6. Find item via OpenFoodFacts API")
    print("7. Exit")
 
 
def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
 
        if choice == "7":
            print("Goodbye!")
            break
 
        action = MENU_ACTIONS.get(choice)
        if action is None:
            print("Invalid option, please try again.")
            continue
 
        action()
 
 
if __name__ == "__main__":
    main()