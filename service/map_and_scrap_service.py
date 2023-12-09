import sys
sys.path.append("..\\scrapper")
sys.path.append("..")
from scrapper import parse_coupa_file
from g2_gateway import *
from utils import *

########################################################################################

def get_uline_item_number(desc):
    h_item_idx = desc.find("H-")
    s_item_idx = desc.find("S-")

    if isValidIndex(h_item_idx):
        return get_item_from_index(h_item_idx, desc)

    if isValidIndex(s_item_idx):
        return get_item_from_index(s_item_idx, desc)

    raise ValueError("Cannot find item number for description: " + desc)    

########################################################################################

def get_item_from_index(idx, desc):
    end_idx = desc[idx:].find(" ")
    if isValidIndex(end_idx):
        return desc[idx:end_idx]
    return desc[idx:]            

########################################################################################
        
def parse_order_from_email(file):
    with open(file, encoding=UTF8) as po:
        order = parse_coupa_file(po)

        items = order.order_lines
        #bill_to = order.bill_to
        ship_to = order.ship_to
        contact = order.contact

        req = {}
        for item in items:
            req[get_uline_item_number(item.description)] = int(item.quantity)
        order.order_lines = req

        runner(req, ship_to, contact)

########################################################################################    

def add_lines(cr_id, num_qty_dict):
    for model, qty in num_qty_dict.items():
        line = line_preperation(model, qty).line
        ext_prc = line.extendedPrice
        item_id = line.itemId
        checkout_request = add_line(cr_id, item_id, qty, ext_prc)

    return checkout_request    

########################################################################################

def map_shipto_address(ship_to):
    return {
        ADDRESS_LINE1: ship_to[1],
        CITY: get_city(ship_to[2]),
        ZIP: get_zipcode(ship_to[2]),
        STATE: get_state(ship_to[2])
    }

########################################################################################    

def map_contact_address(address):
    return {
        ADDRESS_LINE1: address.addressLine1,
        CITY: address.city,
        ZIP: address.zipCode,
        STATE: address.state
    }
    

########################################################################################

def get_customer(ship_to, contact):
    address = map_shipto_address(ship_to)
    uline_shipto_pageable = search_customer(address)
    if isNotEmpty(uline_shipto_pageable.content):
        return match_customer(uline_shipto_pageable, address)

    else:
        address = map_contact_address(contact.customerAddress)
        uline_shipto_pageable = search_customer(address)
        if isNotEmpty(uline_shipto_pageable):
            return match_customer(uline_shipto_pageable, address)

        else:
            raise FileNotFoundError("No matching results for ship-to contact ID: " + str(contact.contactId)) 

########################################################################################

def runner(model_number_qty_dict, ship_to, contact):
    g2_order_number = get_order_number()
    uline_contact = search_contact(contact.name, contact.email)
    shipToCustomer = get_customer(ship_to, uline_contact)

    checkout_request = create_checkout_request(g2_order_number, shipToCustomer, uline_contact)
    checkout_request_id = checkout_request.generalInfo.checkoutRequestId
    checkout_request = add_lines(checkout_request_id, model_number_qty_dict)  
    checkout_request = compute_order_summary(checkout_request_id)

    print(checkout_request)
    checkout_order = submit_checkout_request(g2_order_number, checkout_request_id, shipToCustomer, uline_contact)
    print(checkout_order)
    
########################################################################################

# TODO: PASS EMAILS INTO HERE INSTEAD OF BY NAME
parse_order_from_email(input("Input file name: "))
