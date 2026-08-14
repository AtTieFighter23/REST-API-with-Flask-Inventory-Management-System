"""
Integration with the OpenFoodFacts API for fetching product details
by barcode or product name.
"""

import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (student-lab@example.com)"}


def fetch_by_barcode(barcode):
    """
    Look up a single product by barcode.

    Returns the product dict on success, or None if not found
    or the request fails.
    """
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    return data.get("product")


def fetch_by_name(name):
    """
    Search for products matching a name and return the first result.

    Returns the product dict on success, or None if no results
    or the request fails.
    """
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()
    products = data.get("products", [])

    if not products:
        return None

    return products[0]