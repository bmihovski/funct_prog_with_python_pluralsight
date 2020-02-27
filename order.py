from functools import reduce, lru_cache

from immutable import Immutable
from order_item import OrderItem


def get_updated_tuple(it, predicate, func):
    return tuple(
        func(i) if predicate(i) else i
        for i in it
    )


class Order(Immutable):
    __slots__ = ("order_id", "shipping_address", "expedited",
                 "shipped", "customer", "order_items")
    # class attribute
    orders = []

    def __init__(self, order_id, shipping_address, expedited, shipped, customer, order_items):
        self.order_id = order_id
        self.shipping_address = shipping_address
        self.expedited = expedited
        self.shipped = shipped
        self.customer = customer
        self.order_items = order_items

    @staticmethod
    def count_expedited_orders_with_backordered_items_tramp(orders, acc=0):
        """
            Sample call using tramp function:
                tramp(count_expedited_orders_with_backordered_items_tramp, orders)
        """
        if len(orders) == 0: # also: if not orders
            yield acc
        else:
            h = orders[0]
            add = 1 if any(i.back_ordered for i in h.order_items if h.expedited) else 0
            yield Order.count_expedited_orders_with_backordered_items_tramp(orders[1:], acc + add)

    @property
    @lru_cache(maxsize=1)
    def total_price(self):
        return reduce(lambda acc, x: acc + x.total_price, self.order_items, 0)

    @staticmethod
    def mark_back_ordered(orders, order_id, item_number):
        return Order.map_orders(lambda i:
                                # copy all orders that do not match the order_id
                                i if i.order_id != order_id
                                # otherwise build a new order with a new order item list
                                else (Order(i.order_id, i.shipping_address, i.expedited, i.shipped, i.customer,
                                            Order.map_orders(lambda o:
                                                             # copy the items that don't match
                                                             o if o.item_number != item_number
                                                             # otherwise build a new order item setting backordered to True
                                                             else
                                                             OrderItem(o.name, o.item_number, o.quantity, o.price,
                                                                       True),
                                                             # iterate over all order items
                                                             i.order_items
                                                             ))),

                                # iterate over all orders
                                orders
                                )

    @staticmethod
    def notify_back_ordered(orders, msg):
        Order.get_filtered_info(
            lambda x: any(i.back_ordered for i in x.order_items),
            lambda o: o.customer.notify(o.customer, msg),
            orders
        )

    @staticmethod
    def test_expedited(order):
        return order.expedited

    @staticmethod
    def test_not_expedited(order):
        return not order.expedited

    @staticmethod
    def test_shipped(order):
        return order.shipped

    @staticmethod
    def test_not_shipped(order):
        return not order.shipped

    @staticmethod
    def get_customer_name(order):
        return order.customer.name

    @staticmethod
    def filter_orders(predicate, it):
        return list(filter(predicate, it))

    @staticmethod
    def map_orders(func, it):
        return list(map(func, it))

    @staticmethod
    def get_filtered_info(predicate, func, orders):
        return Order.map_orders(func, Order.filter_orders(predicate, orders))

    @staticmethod
    def get_order_by_id(order_id, orders):
        return filter(lambda order: order.order_id == order_id, orders)

    @staticmethod
    def get_expedited_orders_customer_names():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_name
        )

    @staticmethod
    def get_customer_address(order):
        return order.customer.address

    @staticmethod
    def get_expedited_orders_customer_addresses():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_address
        )

    @staticmethod
    def get_order_shipping_address(order):
        return order.shipping_address

    @staticmethod
    def get_expedited_orders_shipping_addresses():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_order_shipping_address
        )

    @staticmethod
    def get_not_expedited_orders_customer_names():
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_customer_name
        )

    @staticmethod
    def get_not_expedited_orders_customer_addresses():
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_customer_address
        )

    @staticmethod
    def get_not_expedited_orders_shipping_addresses():
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_order_shipping_address
        )

    @staticmethod
    def get_not_shipped_orders_customer_names():
        return Order.get_filtered_info(
            Order.test_not_shipped(),
            Order.get_customer_name
        )

    @staticmethod
    def get_not_shipped_orders_customer_addresses():
        return Order.get_filtered_info(
            Order.test_not_shipped,
            Order.get_customer_address
        )

    @staticmethod
    def get_not_expedited_orders_shipping_addresses():
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_order_shipping_address
        )

    @staticmethod
    def set_order_expedited(order_id, orders, is_expedited):
        for order in Order.get_order_by_id(order_id, orders):
            order.expedited = is_expedited

    @staticmethod
    def set_order_shipped(order_id, orders, is_shipped):
        for order in Order.get_order_by_id(order_id, orders):
            order.shipped = is_shipped
