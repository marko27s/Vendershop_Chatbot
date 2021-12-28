from vendorshop.extensions import db
from vendorshop.order.models import Order, OrderItem, ShippingMethod
from vendorshop.product.models import Product

from constants import *


def get_products(page, option) -> str:

    if option == "next":
        page += 1
    elif option == "back":
        page -= 1

    if page < 1:
        page = 1
    products = Product.query.paginate(page=page, error_out=False, per_page=3).items
    products_list = [f"{p.id} - {p.name} - ${p.min_threshold_amount}" for p in products]
    if len(products_list) == 0:
        return get_products(page, "back")
    return page, "<br>".join(products_list + [SELECT_MESSAGE_BY_ID, PAGINATION])


def get_product(product_id) -> str:
    product = Product.query.filter(Product.id == int(product_id)).first()
    if product is None:
        return INVALID_PRODUCT_ID
    return (
        product,
        f"""
        Product ID: {product.id}<br>
        Product Name: {product.name}<br>
        Description: {product.description}<br>
        Stock: {product.stock}<br>
        Price: ${product.min_threshold_amount}
    """
        + ADD_TO_CART,
    )


def subtract_product(product_id, quantity):
    product = Product.query.filter(Product.id == int(product_id)).first()
    product.stock -= quantity
    db.session.commit()


def get_order_by_id(order_id, user_id):
    
    order = Order.query.filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if order is None:
        return INVALID_ID
    
    return f"""
    <br><br>
    Order ID: {order.id}<br>
    Status: {order.status}<br>
    Date: {order.created_at}<br>
    <br>
    Items:
    <br>
    {'<br>'.join([
        f"{_id+1} - {item.product.name}, Quantity: {item.amount}"
        for _id, item in enumerate(order.items)
    ])}
    <br><br>
    Total Price: ${order.total}
    """


def get_order_by_user(user_id, page, option):
    
    if option == "next":
        page += 1
    elif option == "back":
        page -= 1

    if page < 1:
        page = 1

    orders = (
        Order.query.filter(Order.user_id == user_id)
        .paginate(page=page, error_out=False, per_page=3)
        .items
    )
    if len(orders) == 0:
        return get_order_by_user(user_id, page, "back")

    response = ""
    for order in orders:
        response += f"""
        <br><br>
        Order ID: {order.id}, Status: {order.status}
        <br>
        Total Price: ${order.total}
        """
    response += """
    <br><br>
    Type Order ID for details.<br>
    Type next for more orders<br>
    """
    return page, response


def get_shipping_methods():
    shipping_methods = ShippingMethod.query.all()
    return (
        "<br>".join(
            [
                f"{shipping_method.id} - {shipping_method.name}, Weight: {shipping_method.weight}, Price: {shipping_method.price}"
                for shipping_method in shipping_methods
            ]
        )
        + """
    <br>
    Select from above shipping methods using its ID.
    """
    )


def get_shipping_method(shipping_method_id):
    return ShippingMethod.query.filter(ShippingMethod.id == shipping_method_id).first()


def get_payment_methods():
    return (
        "<br>".join(
            [
                f"{_id} - {PAYMENT_METHODS[_id]['name']}"
                for _id in PAYMENT_METHODS.keys()
            ]
        )
        + """
    <br>
    Select from above payment methods using its ID.
    """
    )
