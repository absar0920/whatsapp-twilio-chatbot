from session import SessionLocal
from models import Product
from typing import List

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig



@tool
def get_products(query: str, limit: int = 10, config: RunnableConfig = {}):
    """
        List products in the datbase,
         
        @params:
            query: the keywords to search for the products, it will used in product name and in description
         default limit is 10, but can be increased and use -1 for all products at once.
    """
    db = SessionLocal()
    results: List[Product] = db.query(Product).filter(
        (Product.name.ilike(f"%{query}%")) |
        (Product.description.ilike(f"%{query}%"))
    ).all()
    if limit > 0:
        results[:limit]
    db.close()
    if not results:
        return "No products found."
    return "\n".join([
        f"- {p.name}: ${p.price} (Stock: {p.stock})\n  Description: {p.description}" for p in results
    ])


@tool
def get_product_details(product_id: int, config: RunnableConfig = {}):
    """
        Get product details based on it's product_id
    """

    print("called get_product_details tool with product_id: ", product_id)

    db = SessionLocal()
    p: Product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not p:
        return "No product found"
    
    return {dict(p)}

