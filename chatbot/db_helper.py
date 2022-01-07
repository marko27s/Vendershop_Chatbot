from vendorshop.admin.models import Notification
from vendorshop.extensions import db
from vendorshop.order.models import Order, OrderItem, ShippingMethod
from vendorshop.payment.models import Payment
from vendorshop.product.models import Product
from vendorshop.ticket.models import Ticket, TicketMessage
from vendorshop.user.models import User

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


def get_payment_details():
    pass


def get_order_by_id(order_id, user_id):

    order = Order.query.filter(Order.id == order_id, Order.user_id == user_id).first()

    if order is None:
        return INVALID_ID

    return (
        f"""
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
    Total Price in USD: ${order.total}<br><br>
    Wallet Address<br>
    {order.payment.address}<br>
    {PAYMENT_APPEAR_TIME}<br><br>
    Payment method: {order.payment.currency}<br>
    Order Value: {order.payment.amount}<br><br>
    """
        + CREATE_TICKET
    )


def get_items_by_order_id(order_id, user_id):

    order = Order.query.filter(Order.id == order_id, Order.user_id == user_id).first()

    if order is None:
        return INVALID_ID

    return (
        f"""
    <br><br>
    Order ID: {order.id}<br>
    <br>
    Items:
    <br>
    {'<br>'.join([
        f"{item.id} - {item.product.name}, Quantity: {item.amount}"
        for _id, item in enumerate(order.items)
    ])}
    <br><br>
    """
        + SELECT_ITEM_ID
    )


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


def create_notifications_for_seller(user, order_item):

    notification = Notification(
        text=f"{user.username} placed an order, ORDER # {order_item.order.id}",
        link=f"{WEB_UI_BASE_URL}order/{order_item.order.id}",
        user=order_item.product.user,
    )
    notification.save()


def get_latest_notifications_for_the_user(user_id, page, option):
    if option == "next":
        page += 1
    elif option == "back":
        page -= 1

    if page < 1:
        page = 1
    notifications_paginate = (
        Notification.query.filter(Notification.user_id == user_id)
        .order_by(Notification.id.desc())
        .paginate(page=page, error_out=False, per_page=5)
        .items
    )
    notifications = [f"{n.text}" for n in notifications_paginate]
    if len(notifications) == 0:
        return get_latest_notifications_for_the_user(user_id, page, "back")
    return page, "<br>".join(notifications + [PAGINATION])


def create_ticket_for_the_order(user_id, item_id, subject, message):
    user = User.query.filter(User.id == user_id).first()

    item = OrderItem.query.filter(OrderItem.id == int(item_id)).first()

    ticket = Ticket(
        subject=subject, order_id=item.order_id, seller_id=item.product.user_id
    )
    ticket.messages.append(
        TicketMessage(message=message),
    )
    user.tickets.append(ticket)
    user.commit()

    return TICKET_CREATED


def get_all_tickets_for_the_user(user_id, page, option):
    if option == "next":
        page += 1
    elif option == "back":
        page -= 1

    if page < 1:
        page = 1

    tickets_paginate = (
        Ticket.query.filter(Ticket.user_id == user_id)
        .order_by(Ticket.id.desc())
        .paginate(page=page, error_out=False, per_page=3)
        .items
    )
    tickets = [f"{t.id} - {t.subject}" for t in tickets_paginate]
    if len(tickets) == 0:
        return get_all_tickets_for_the_user(user_id, page, "back")
    return page, "<br>".join(tickets + [PAGINATION])


def get_ticket_from_id(user_id, ticket_id):
    ticket = Ticket.query.filter(
        Ticket.id == ticket_id, Ticket.user_id == user_id
    ).first()

    if ticket is None:
        return INVALID_ID

    messages = ""
    for message in ticket.messages:
        title = "Seller" if message.admin else "You"
        messages += f"""
        {title}: {message.message}<br><br>
        """

    return messages + "Type any message for the reply.<br>"


def send_message_for_ticket(ticket_id, message):
    ticket = Ticket.query.filter(Ticket.id == ticket_id).first()
    ticket_message = TicketMessage(admin=False, message=message)
    ticket.messages.append(ticket_message)
    ticket.commit()

    return "Message Sent!"
