"""
In-memory inventory storage.

Each item is a dict shaped loosely like OpenFoodFacts product data,
plus fields specific to our inventory system (id, price, stock).
"""

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 4.99,
        "stock": 25,
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Dave's Killer Bread",
        "ingredients_text": "Whole wheat flour, water, yeast, honey",
        "price": 5.49,
        "stock": 12,
    },
]