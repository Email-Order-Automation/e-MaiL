from enum import Enum

class OrderLine:
    def __init__(self, sequence, description, need_by_date, quantity, unit, price, total):
        self.sequence = sequence
        self.description = description
        self.need_by_date = need_by_date
        self.quantity = quantity
        self.unit = unit
        self.price = price
        self.total = total

class Rows(Enum):
    LINE_NUM = 0
    DESCRIPTION = 1
    NBD = 2
    QTY = 3
    UNIT = 4
    PRICE = 5
    TOTAL = 6