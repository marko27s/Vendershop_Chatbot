from vendorshop.product.models import Product
from vendorshop.order.models import ShippingMethod

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
        return get_products(page, "back") + "<br>"
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


def get_shipping_methods():
    shipping_methods = ShippingMethod.query.all()
    return '<br>'.join([
        f"{shipping_method.id} - {shipping_method.name}, Weight: {shipping_method.weight}, Price: {shipping_method.price}"
        for shipping_method in shipping_methods
    ]) + """
    <br>
    Select from above shipping methods using its ID.
    """


def get_shipping_method(shipping_method_id):
    return ShippingMethod.query.filter(ShippingMethod.id == shipping_method_id).first()


def get_payment_methods():
    return '<br>'.join([
        f"{_id} - {PAYMENT_METHODS[_id]['name']}"
        for _id in PAYMENT_METHODS.keys()
    ]) + """
    <br>
    Select from above payment methods using its ID.
    """
