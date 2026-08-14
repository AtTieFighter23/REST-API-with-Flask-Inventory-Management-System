# Inventory Management System

A Flask-based REST API with CRUD operations for managing an e-commerce
inventory, enriched with real-time product data from the
[OpenFoodFacts API](https://world.openfoodfacts.org/). Includes a
command-line interface for interacting with the API without needing
a separate front end.

## Features

- Full CRUD REST API (`GET`, `POST`, `PATCH`, `DELETE`) for inventory items
- External product lookup by barcode or name via the OpenFoodFacts API
- CLI tool to add, view, update, delete, and search for inventory items
- Automated test suite (pytest + unittest.mock) covering the API, CLI,
  and external API integration without hitting the network in tests

## Project Structure

```
.
├── app.py              # Flask app and REST API routes
├── data.py             # In-memory inventory data store
├── external_api.py     # OpenFoodFacts API integration
├── cli.py              # Command-line interface
├── Pipfile / Pipfile.lock
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_cli.py
│   └── test_external_api.py
└── README.md
```

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:AtTieFighter23/REST-API-with-Flask-Inventory-Management-System.git
   cd REST-API-with-Flask-Inventory-Management-System
   ```

2. Install dependencies with Pipenv (requires Python 3.12):
   ```bash
   pipenv install
   ```

3. Activate the environment (or prefix commands with `pipenv run`):
   ```bash
   pipenv shell
   ```

## Running the API Server

```bash
python app.py
```

The server runs on `http://localhost:5000` by default.

## Running the CLI

With the API server running in one terminal, open another terminal and run:

```bash
python cli.py
```

You'll see a menu:

```
--- Inventory Management CLI ---
1. View all items
2. View item details
3. Add new item
4. Update item price/stock
5. Delete item
6. Find item via OpenFoodFacts API
7. Exit
Choose an option:
```

### Example: Adding an item manually

```
Choose an option: 3
Product name: Grass Fed Beef
Brand (optional): Hyatt
Price (optional, default 0.0): 10.99
Stock (optional, default 0): 36
Item added successfully:
  ID: 3
  Product Name: Grass Fed Beef
  Brands: Hyatt
  Price: $10.99
  Stock: 36
```

### Example: Finding a product via OpenFoodFacts

```
Choose an option: 6
Search by (b)arcode or (n)ame? b
Enter barcode: 3017624010701
Found: Nutella (Ferrero)
Add this item to inventory? (y/n): y
Item added successfully:
  ID: 4
  Product Name: Nutella
  ...
```

## API Endpoints

| Method | Endpoint             | Description                          |
| ------ | --------------------- | ------------------------------------- |
| GET    | `/`                    | Welcome message                       |
| GET    | `/inventory`           | Fetch all inventory items             |
| GET    | `/inventory/<id>`      | Fetch a single item by ID             |
| POST   | `/inventory`           | Add a new item (`product_name` required) |
| PATCH  | `/inventory/<id>`      | Update fields on an existing item     |
| DELETE | `/inventory/<id>`      | Remove an item                        |

### Example: `POST /inventory`

Request body:
```json
{
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "price": 4.99,
  "stock": 25
}
```

Response (`201 Created`):
```json
{
  "id": 3,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "",
  "price": 4.99,
  "stock": 25
}
```

## External API Notes

This project uses the [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/)
to enrich inventory data:

- Barcode lookup: `GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json`
- Name search: `GET https://world.openfoodfacts.org/cgi/search.pl` (legacy endpoint,
  since full-text search isn't available in API v2)

OpenFoodFacts enforces rate limits (15 req/min for product reads, 10 req/min
for search), so the CLI is designed for interactive, on-demand lookups rather
than bulk fetching.

## Running Tests

```bash
pipenv run pytest tests/ -v
```

All external network calls (both to the OpenFoodFacts API and between the
CLI and the Flask server) are mocked in tests, so the test suite runs
offline and doesn't require the Flask server to be running.

## Notes on Data Persistence

Inventory data is stored in-memory (`data.py`) and resets whenever the
Flask server restarts. This satisfies the lab's "simulated data storage"
requirement; a real deployment would replace this with a database.