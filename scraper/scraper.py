from bs4 import BeautifulSoup
from scraper_models import *
from pprint import pprint
import re

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

        for cells in fields:

            text = re.sub(' +', ' ', cells.get_text().strip().replace("\n", ""))
            stripped_fields_list.append(text)

            if len(stripped_fields_list) == 7:
                line_items.append(map_fields(stripped_fields_list))

    return line_items  

########################################################################################

def parse_coupa_file(order_file):
    order = BeautifulSoup(order_file, "html.parser")
    lines = order.find(id="order_lines").find_all('tr')
    return strip_po_data(lines)

########################################################################################
