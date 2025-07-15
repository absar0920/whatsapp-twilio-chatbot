from session import SessionLocal
from models import Product, Order
from typing import List
import json

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def get_products(query: str, limit: int = 10, config: RunnableConfig = {}):
    """
    List products in the datbase,

    @params:
        query: the keywords to search for the products, it will used in product name and in description, if query is None, then no query will be applied
     default limit is 10, but can be increased and use -1 for all products at once.
    """
    print(f"Tool Call: Get products tool called: query={query}, limit={limit}")
    db = SessionLocal()
    results: List[Product] = (
        db.query(Product)
        .filter(
            (
                (Product.name.ilike(f"%{query}%"))
                | (Product.description.ilike(f"%{query}%"))
            )
            if query
            else True
        )
        .all()
    )
    if limit > 0:
        results[:limit]
    db.close()
    if not results:
        return "No products found."
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "description": p.description,
        }
        for p in results
    ]

@tool
def get_product_details(product_id: int, config: RunnableConfig = {}):
    """
    Get product details based on it's product_id
    """
    print(f"Tool Call: Get product details called: {product_id}")
    db = SessionLocal()
    p: Product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if not p:
        return "No product found"

    return f"Product ID: {p.id}, Name: {p.name}, Price: ${p.price:.2f}, Stock: {p.stock}, Description: {p.description}"

@tool
def get_orders_for_a_customer(customer_name: str, config: RunnableConfig = {}):
    """
    Get Orders for a customer based on the customers name
    """
    print(f"Tool Called: get order for the customer, customer_name={customer_name}")
    db = SessionLocal()
    orders: List[Order] = (
        db.query(Order).filter(Order.customer_name.ilike(customer_name)).all()
    )

    print(f"order for customer: {customer_name}.", [o.id for o in orders])
    db.close()
    if not orders or len(orders) == 0:
        return "The customer does not have any orders"

    return "\n".join(
        [
            f"Order ID: {o.id}, Product ID: {o.product_id}, Product Name: {o.product_id.name}, Quantity: {o.quantity}, Total Price: ${o.total_price:.2f}, Status: {o.status}"
            for o in orders
        ]
    )

@tool
def generate_order(
    customer_name: str, product_id: int, phone_number: str, config: RunnableConfig = {}
):
    """
    Create order against a customer with their name and a product id and phone_number.
    Checks product existence and stock, creates the order, updates stock, and returns order details or an error message.
    Prevents duplicate order creation for the same customer and product in a short time window.
    """
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        db.close()
        return f"No product found with id {product_id}."
    existing_order = (
        db.query(Order)
        .filter(
            Order.customer_name == customer_name,
            Order.product_id == product_id,
            Order.status == "pending"
        )
        .order_by(Order.created_at.desc())
        .first()
    )
    if existing_order:
        db.close()
        return (
            f"Order already created recently!\n"
            f"Customer: {customer_name}\n"
            f"Product: {product.name}\n"
            f"Quantity: {existing_order.quantity}\n"
            f"Total Price: ${existing_order.total_price:.2f}\n"
            f"Order Status: {existing_order.status}"
        )
    print(
        f"Tool Called: with details: customer_name={customer_name} product_id={product_id} phone_number={phone_number}"
    )
    quantity = 1
    total_price = product.price * quantity

    order = Order(
        product_id=product.id,
        quantity=quantity,
        total_price=total_price,
        customer_name=customer_name,
        customer_phone=phone_number,
        status="pending",
    )
    db.add(order)
    product.stock -= quantity
    db.commit()
    db.refresh(order)
    db.close()
    statement = (
        f"Order created!\n"
        f"Customer: {customer_name}\n"
        f"Product: {product.name}\n"
        f"Quantity: {quantity}\n"
        f"Total Price: ${total_price:.2f}\n"
        f"Order Status: {order.status}"
    )
    return statement
