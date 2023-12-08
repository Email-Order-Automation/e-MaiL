from bs4 import BeautifulSoup
from scrapper_models import *
from pprint import pprint
import sys
sys.path.append("..")
from uline_utils import *

########################################################################################

SHIP_TO = "Ship To"
BILL_TO = "Bill To"
CONTACT = "CONTACT"

########################################################################################

def map_line_fields(fields_list):
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
    else:
        raise ValueError("Not enough information found on order email")    

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
                line_items.append(map_line_fields(stripped_fields_list))

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

def strip_contact_data(table, label_idx, rows, row_idx):
    name = get_element_content(table[label_idx + 1])
    email_data = rows[row_idx + 1].find_all('td')
    email = get_element_content(email_data[1])

    return Contact(name, email)

########################################################################################

def strip_contact_info(po_info):
    rows = po_info.find_all('tr')

    row_idx = 0
    for row in rows:
        table_data = row.find_all('td')

        contact_label_idx = 0
        for cell in table_data:
            text = get_element_content(cell)

            if text == "CONTACT":
                return strip_contact_data(table_data, contact_label_idx, rows, row_idx)

            contact_label_idx += 1
        row_idx += 1

########################################################################################

def parse_coupa_file(order_file):
    order = BeautifulSoup(order_file, "html.parser")

    lines = order.find(id="order_lines").find_all('tr')
    order_lines = strip_po_data(lines)
    if not order_lines:
        raise ValueError("Can't find order line information on order email")

    address_data = order.find(id="addresses")
    bill_to = strip_order_address(address_data, BILL_TO)
    ship_to = strip_order_address(address_data, SHIP_TO)
    if not ship_to:
        raise ValueError("Can't find ship-to information on order email")
    
    po_info = order.find(id="po_info")
    contact = strip_contact_info(po_info)
    if not contact:
        raise ValueError("Can't find contact information on order email")

    return Order(order_lines, bill_to, ship_to, contact)

########################################################################################