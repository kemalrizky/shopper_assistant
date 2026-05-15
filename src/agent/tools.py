from typing import Optional, Literal
from src.db.mongo import manual_collection, products_collection
from src.db.embeddings import embed_query
from src.config import MANUAL_INDEX_NAME, PRODUCTS_INDEX_NAME

def format_manual_results(results: list) -> str:
    """Format manual search results into readable string for the agent."""
    if not results:
        return "No relevant information found in the Tokoku user manual."

    formatted = []
    for i, r in enumerate(results):
        formatted.append(
            f"[{i+1}] Topic: {r['topic']}\n"
            f"    Information: {r['information']}"
        )
    return "\n\n".join(formatted)

def format_product_results(results: list) -> str:
    """Format product search results into readable string for the agent."""
    if not results:
        return "No products found matching the search criteria."

    formatted = []
    for i, r in enumerate(results):
        stock = "In Stock" if not r.get("out_of_stock") else "Out of Stock"
        formatted.append(
            f"[{i+1}] {r['title']}\n"
            f"    Brand    : {r['brand']}\n"
            f"    Category : {r.get('sub_category', 'N/A')}\n"
            f"    Price    : {r.get('selling_price_formatted', 'N/A')} "
            f"(was {r.get('actual_price_formatted', 'N/A')}, {r.get('discount', 'N/A')})\n"
            f"    Stock    : {stock}\n"
            f"    Relevance: {r.get('score', 0):.2f}\n"
            f"    {r.get('description', '')[:150]}..."
        )
    return "\n\n".join(formatted)

def search_manual(query: str) -> str:
    """Search the Tokoku user manual to answer customer support questions.
    Use this when the customer asks about:
    - how to use a platform feature
    - account issues (login, registration, verification)
    - order tracking, cancellation, or modification
    - payment methods or billing problems
    - return and refund policies
    - seller-related questions
    - shipping and delivery questions
    - platform policies and rules

    Do NOT use this for product recommendations or catalog searches.

    Args:
        query: the customer's question in natural language
    """
    if manual_collection is None:
        return "Error: Database connection not established."

    results = list(manual_collection.aggregate([
        {
            "$vectorSearch": {
                "index": MANUAL_INDEX_NAME,
                "path": "embedding",
                "queryVector": embed_query(query),
                "numCandidates": 50,
                "limit": 2
            }
        },
        {
            "$project": {
                "topic": 1,
                "information": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]))
    return format_manual_results(results)

def search_products(
    query: str,
    min_price: int = 0,        
    max_price: int = 0,        
    min_discount_pct: int = 0, 
    sub_category: str = "",    
    in_stock_only: bool = False,
    limit: int = 3
) -> str:
    """Search the Tokoku product catalog to find items matching the customer's needs. 
    Use this when the customer:
    - asks for product recommendations
    - mentions a category (e.g. jacket, shoes, t-shirt, bag)
    - specifies a budget or price range
    - asks about discounts or sale items
    - wants to check what is currently in stock
    - describes what they are looking for

    Do NOT use this for platform policy or account questions.

    Args:
        query          : natural language description of what the customer wants
        min_price      : minimum price in IDR integers (e.g. 100000) (0 = no minimum)
        max_price      : maximum price in IDR integers (e.g. 200000) (0 = no maximum)
        min_discount_pct: minimum discount percentage (e.g. 30 for at least 30% off) (0 = no minimum)
        sub_category   : exact category, must be one of:
                         "Tops & T-Shirts" (for baju, kaos, kemeja, atasan),
                         "Bottoms & Pants" (for celana, rok, bawahan),
                         "Footwear" (for sepatu, sandal),
                         "Jackets & Outerwear" (for jaket, sweater, hoodie),
                         "Fashion Accessories" (for topi, sabuk, jam tangan),
                         "Bags & Wallets" (for tas, dompet).
                         If specified, must match EXACTLY one of the English keys above. ("" = all categories)
        in_stock_only  : set True if customer explicitly wants available items only
        limit          : number of results to return, default 3, max 10.
                         Use higher value only if customer asks for more options.
    """
    if products_collection is None:
        return "Error: Database connection not established."

    if isinstance(min_price, str):
        min_price = int(min_price.replace(",", "").replace(".", ""))
    if isinstance(max_price, str):
        max_price = int(max_price.replace(",", "").replace(".", ""))
    if isinstance(min_discount_pct, str):
        min_discount_pct = int(min_discount_pct)
    if isinstance(limit, str):
        limit = int(limit)

    limit = min(max(1, limit), 10)

    # build filter conditions
    filter_conditions = {}
    price_filter = {}
    if min_price > 0:
        price_filter["$gte"] = min_price
    if max_price > 0:
        price_filter["$lte"] = max_price
    if price_filter:
        filter_conditions["selling_price"] = price_filter
    if min_discount_pct > 0:
        filter_conditions["discount_pct"] = {"$gte": min_discount_pct}
    if sub_category:
        filter_conditions["sub_category"] = sub_category
    if in_stock_only:
        filter_conditions["out_of_stock"] = False

    vector_search_stage = {
        "$vectorSearch": {
            "index": PRODUCTS_INDEX_NAME,
            "path": "embedding",
            "queryVector": embed_query(query),
            "numCandidates": max(100, limit * 20),
            "limit": limit,
        }
    }

    if filter_conditions:
        vector_search_stage["$vectorSearch"]["filter"] = filter_conditions

    pipeline = [
        vector_search_stage,
        {
            "$project": {
                "title": 1,
                "brand": 1,
                "sub_category": 1,
                "selling_price_formatted": 1,
                "actual_price_formatted": 1,
                "discount": 1,
                "discount_pct": 1,
                "out_of_stock": 1,
                "description": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    results = list(products_collection.aggregate(pipeline))
    return format_product_results(results)
