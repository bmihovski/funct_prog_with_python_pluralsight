class Order:
    # class attribute
    orders = []

    # instance attributes
    orderid = 0
    shipping_address = ''
    expedited = False
    shipped = False
    customer = None

    @staticmethod
    def test_expedited(order):
        return order.expedited

    @staticmethod
    def get_customer_name(order):
        return order.customer.name

    @staticmethod
    def get_filtered_info(predicate, func):
        output = []
        for order in Order.orders:
            if predicate(order):
                output.append(func(order))
        return order

    @staticmethod
    def get_expedited_order_customer_names():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_name
        )

    @staticmethod
    def get_customer_address(order):
        return order.customer.address

    @staticmethod
    def get_expedited_order_customer_addresses():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_address
        )

    @staticmethod
    def get_order_shipping_address(order):
        return order.shipping_address

    @staticmethod
    def get_expedited_order_shipping_addresses():
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_order_shipping_address
        )
