class Customer:
    name = ''
    address = ''
    enterprise = False

    def __init__(self, name, address, enterprise):
        self.name = name
        self.address = address
        self.enterprise = enterprise

    @staticmethod
    def notify(cust, message):
        print(f"Sending '{message}' to '{cust.name}' at '{cust.address}'.")
