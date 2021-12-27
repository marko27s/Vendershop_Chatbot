from vendorshop.extensions import db
from vendorshop.user.models import (
    User
)
from vendorshop.order.models import (
    Order, OrderItem, ShippingMethod
)
from vendorshop.payment.models import (
    Payment
)
from vendorshop.admin.models import (
    convert_price
)
from chatbot.db_helper import get_product, get_shipping_method
from constants import *


class Cart:
    """
    For saving items in the cart
    """

    def __init__(self, shiiping_address) -> None:
        self.items = {}
        self.shiiping_address = shiiping_address
        self.shipping_method = None
        self.payment_method = None
        self.refund_address = None

    def set_shipping_address(self, shiiping_address):
        self.shiiping_address = shiiping_address
    
    def set_refund_address(self, refund_address):
        self.refund_address = refund_address
        return REFUND_ADDRESS_SET_AKW + PROCEED

    def set_payment_method(self, payment_method_id) -> None:
        self.payment_method = PAYMENT_METHODS.get(payment_method_id)
        if self.payment_method is None:
            return INVALID_ID
        return f"""
        Payment Method Set.{PROCEED}
        """

    def set_shipping_method(self, shipping_id):
        shipping_method = get_shipping_method(shipping_id)
        if shipping_method is None:
            return INVALID_ID
        self.shipping_method = shipping_method
        return f"""
        Shipping Method Set.{PROCEED}
        """
    
    def get_shipping_address(self):
        return f"""
        Your Shipping Address: {self.shiiping_address}<br>
        Type update new_shipping_address
        """ + PROCEED 

    def remove_product(self, product_id) -> None:
        try:
            del self.items[product_id]
        except:
            pass

    def add_product(self, product, quantity) -> str:
        product, _ = get_product(product.id)
        if product is None:
            return INVALID_PRODUCT_ID

        if product.stock < quantity:
            return STOCK_UNAILABLE

        self.items[product.id] = [
            product.name,
            product.description,
            product.get_unit_price(quantity),
            quantity,
        ]
        return PRODUCT_ADDED_TO_CART

    def update_product(self, product_id, quantity) -> str:
        product, _ = get_product(product_id)
        if product is None:
            return INVALID_PRODUCT_ID

        if product.stock < quantity:
            return STOCK_UNAILABLE

        self.items[product.id] = [
            product.name,
            product.description,
            product.get_unit_price(quantity),
            quantity,
        ]
        return PRODUCT_UPDATED

    def get_cart_items(self) -> str:
        if len(list(self.items.keys())) == 0:
            return ""
        return "-----<br>" + "<br>".join(
            [
                f"{_id}, {self.items[_id][0]}, ${self.items[_id][2]*self.items[_id][3]}, {self.items[_id][3]}"
                for _id in self.items.keys()
            ]
        ) + "<br>-----"

    def get_total_cost(self):
        totals = sum([
            self.items[_id][2]*self.items[_id][3]
            for _id in self.items.keys()
        ])
        return f"""
        <br>
        Total Items Cost: ${totals}
        """

    def create_order(self, user):
        user = User.query.filter(User.id == user.id).first()
        # creste items list
        product_items = []
        for product_id in self.items.keys():
            p, _ = get_product(product_id)
            product_items.append(
                OrderItem(product=p, amount=self.items[product_id][3])
            )
        order = Order()
        order.items = product_items
        order.shipping_address = self.shiiping_address
        order.shipping_method = ShippingMethod.query.get(
            self.shipping_method.id,
        )
        order.shipping_method_id = self.shipping_method.id
        order.refund_address = self.refund_address
        order.payment = Payment(currency=self.payment_method['value'])
        order.payment.amount = convert_price(
            order.total, order.payment.currency,
        )
        
        user.orders.append(order)
        user.commit()
        return """
        Order Created!
        """

# class Order(db.Model, BaseMixin):
#     __tablename__ = "orders"

#     items = db.relationship("OrderItem")
#     status = db.Column(db.Enum(OrderStatus), default=OrderStatus.unpaid)
#     refund_address = db.Column(db.String(128), nullable=False)
#     shipping_address = db.Column(db.Text(), nullable=False)
#     shipping_method_id = db.Column(
#         db.Integer(), db.ForeignKey("shipping_methods.id"))
#     shipping_method = db.relationship("ShippingMethod")
#     tickets = db.relationship("Ticket")
#     payment = db.relationship(
#         "Payment", uselist=False, back_populates="order")
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     user = db.relationship("User")
