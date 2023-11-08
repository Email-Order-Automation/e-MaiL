from bs4 import BeautifulSoup
from scraper_models import *
from pprint import pprint
import re

SHIP_TO = "Ship To"
BILL_TO = "Bill To"


def get_element_content(stringer):
    return re.sub(' +', ' ', stringer.get_text().strip().replace("\n", ""))

########################################################################################

def map_fields(fields_list):
    seq = fields_list[Rows.LINE_NUM.value]
    desc = fields_list[Rows.DESCRIPTION.value]
    nbd = fields_list[Rows.NBD.value]
    qty = fields_list[Rows.QTY.value]
    unit = fields_list[Rows.UNIT.value]
    price = fields_list[Rows.PRICE.value]
    total = fields_list[Rows.TOTAL.value]

    # Minimum Viable Values
    if seq and desc and qty and unit:
        return OrderLine(seq, desc, nbd, qty, unit, price, total)

########################################################################################

def strip_po_data(lines):
    line_items = []
    for line in lines:
        
        stripped_fields_list = []
        fields = line.find_all('td')

        for cell in fields:

            text = get_element_content(cell)
            stripped_fields_list.append(text)

            if len(stripped_fields_list) == 7:
                line_items.append(map_fields(stripped_fields_list))

    return line_items  

########################################################################################

def strip_order_address(addresses, add_type):
    sets = addresses.find_all('fieldset')
    for fieldset in sets:
        label = fieldset.find('legend')
        lName = get_element_content(label)

        if lName == add_type:
            stripped_fields_list = []
            divs = fieldset.find_all('div')

            for cell in divs:
                text = get_element_content(cell)
                stripped_fields_list.append(text)

            return stripped_fields_list    



########################################################################################

def parse_coupa_file(order_file):
    order = BeautifulSoup(order_file, "html.parser")

    lines = order.find(id="order_lines").find_all('tr')
    order_lines = strip_po_data(lines)

    address_data = order.find(id="addresses")
    bill_to = strip_order_address(address_data, BILL_TO)
    ship_to = strip_order_address(address_data, SHIP_TO)

    return Order(order_lines, bill_to, ship_to)

########################################################################################
