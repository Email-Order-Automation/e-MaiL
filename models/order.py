class Order:
    def __init__(self, billto, shipto, lineItems, orderNumber):
        self.billto = billto
        self.shipto = shipto
        self.lineItems = lineItems
        self.orderNumber = orderNumber
        