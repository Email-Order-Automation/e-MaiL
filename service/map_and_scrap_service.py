import sys
sys.path.append("..\\scrapper")
sys.path.append("..")
from scrapper import parse_coupa_file
from g2_gateway import runner

########################################################################################

def get_uline_item_number(desc):
    h_item_idx = desc.find("H-")
    s_item_idx = desc.find("S-")

    if h_item_idx != -1:
        return get_item_from_index(h_item_idx, desc)

    if s_item_idx != -1:
        return get_item_from_index(s_item_idx, desc)

########################################################################################

def get_item_from_index(idx, desc):
    end_idx = desc[idx:].find(" ")
    if end_idx != -1:
        return desc[idx:end_idx]
    return desc[idx:]            

########################################################################################
        
def build_line_item():
    with open("purchase_order.html", encoding="utf8") as fp:
        order = parse_coupa_file(fp)

        items = order.order_lines
        bill_to = order.bill_to
        ship_to = order.ship_to
        contact = order.contact

        req = {}
        for item in items:
            req[get_uline_item_number(item.description)] = int(item.quantity)

        runner(req, bill_to, ship_to, contact)

########################################################################################

build_line_item()