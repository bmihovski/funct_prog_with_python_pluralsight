class OrderItem:
    name = ''
    item_number = ''
    quantity = 0
    price = 0
    back_ordered = False

    def __init__(self, name, item_number, quantity, price, back_ordered):
        self.name = name
        self.item_number = item_number
        self.quantity = quantity
        self.price = price
        self.back_ordered = back_ordered

    @property
    def total_price(self):
        return self.quantity * self.price
