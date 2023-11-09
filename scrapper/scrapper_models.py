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

########################################################################################

class Address:
    def __init__(self, address1, address2, city, state, postal, postal_ext):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.postal = postal
        self.postal_ext = postal_ext

########################################################################################

class Contact: 
    def __init__(self, name, email):
        self.name = name
        self.email = email

########################################################################################              

class Order:
    def __init__(self, order_lines, bill_to, ship_to, contact):
        self.order_lines = order_lines
        self.bill_to = bill_to
        self.ship_to = ship_to
        self.contact = contact

########################################################################################

class Rows(Enum):
    LINE_NUM = 0
    DESCRIPTION = 1
    NBD = 2
    QTY = 3
    UNIT = 4
    PRICE = 5
    TOTAL = 6
