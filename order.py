class Order:
    # class attribute
    orders = []

    # instance attributes
    orderid = 0
    shipping_address = ''
    expedited = False
    shipped = False
    customer = None


    def get_expedited_order_customer_names(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.customer.name)
        return output


    def get_expedited_order_customer_addresses(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.customer.name)
        return output


    def get_expedited_order_shipping_addresses(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.customer.name)
        return output