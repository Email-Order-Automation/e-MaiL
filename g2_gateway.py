import requests
import json
from client_urls import *
from http_params import *
from urllib.parse import urlencode
from urllib.request import urlretrieve
from utils import *

########################################################################################

def get_uline_token():
    headers = {
        CONTENT_TYPE: APPLICATION_JSON,
        AUTHORIZATION: BASIC
    }

    response = requests.request(POST, SECURITY_AUTH_URL, headers=headers, data="")

    json_data = json.loads(response.text)
    return(json_data[TOKEN])

########################################################################################

ULINE_TOKEN = get_uline_token()
STANDARD_HEADERS = {
        CONTENT_TYPE: APPLICATION_JSON,
        AUTHORIZATION: BEARER + " " + ULINE_TOKEN
    }

########################################################################################

def get_order_number():
    response = requests.request(POST, ORDER_NUMBER_URL, headers=STANDARD_HEADERS, data="{}")
    return json.loads(response.text)[ORDER_NUMBER] + FIVE_BILLION

########################################################################################

def create_checkout_request(order_number, shipToCustomer, contact):
    payload = json.dumps({
        COMPANY_CODE: shipToCustomer.companyCode,
        CATALOG_CODE: FV_CC,
        SOURCE_APPLICATION: JOE_PHONE,
        ORDER_TYPE: WRITTEN_ORDER,
        BILL_TO_CUSTOMER_ID: shipToCustomer.billToId,
        SHIP_TO_CUSTOMER_ID: shipToCustomer.customerId,
        CONTACT_NAME: contact.contactName,
        ORDER_NUMBER: order_number,
        CUSTOMER_PURCHASE_ORDER_NUMBER: G2HOLD,
        KEEP_LOCKED: False,
        MEXICO_USAGE_CODE: POI,
        PAYMENT_TYPE: NET_30,
        AUTO_ASSIGN_NUM: False
    })

    response = requests.request(POST, OES_CHECKOUT_REQ_URL, headers=STANDARD_HEADERS, data=payload)
    return create_object(response.text)

########################################################################################    

def search_customer(address_line, city, customer_name, postal_code, state_province_code):
    url = CUSTOMER_SEARCH_URL
    url += generate_param(ADDRESS_LINE, address_line)
    url += generate_param(CITY, city)
    url += generate_param(POSTAL_CODE, postal_code)
    url += generate_param(STATE_PROV_CODE, state_province_code)
    url += generate_param("markedForDeletion", False)

    response = requests.request(GET, url, headers=STANDARD_HEADERS)
    return create_object(response.text)

########################################################################################

def match_contact(name, email, pageable):
    content = pageable.content
    for contact in content:
        if contact.contactName.lower() == name.lower() and contact.emailAddress.lower() == email.lower():
            return contact

########################################################################################    
    
def search_contact(name, emailAddress):
    url = CONTACT_SEARCH_URL
    url += generate_param(NAME, name)
    url += generate_param(EMAIL, emailAddress)
    url += generate_param("customerMarkedForDeletion", False)

    response = requests.request(GET, url, headers=STANDARD_HEADERS)
    return match_contact(name, emailAddress, create_object(response.text))
    
########################################################################################    

def convert_customer_to_billto(customer):
    url = BILL_TO_URL
    url += generate_param(CUSTOMER_NUMBER, customer.customerId)
    url += generate_param(COMPANY_CODE, customer.companyCode)

    response = requests.request(GET, url, headers=STANDARD_HEADERS)
    return create_object(response.text)

########################################################################################

def add_line(checkout_request_id, item_id, quantity, extended_price):
    payload = json.dumps({
        LINES: [
            {
            ITEM_ID: item_id,
            PRODUCT_ID: None,
            SELLABLE_ORDERED_QTY: quantity,
            EXT_PRICE: extended_price,
            RA_CODE: EMPTY
            }
        ]
        })

    response = requests.request(POST, OES_LINES_URL.format(checkout_request_id), headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

########################################################################################    

def compute_order_summary(checkout_request_id):
    response = requests.request(POST, OES_SUMMARY_URL.format(checkout_request_id), headers=STANDARD_HEADERS, data="{}")
    return json.loads(response.text)

########################################################################################

def line_preperation(model_number, quantity):
    payload = json.dumps({
        COMPANY_CODE : US_COMP_CODE,
        MODEL_NUM : model_number,
        QTY : quantity,
        RA_CODE : EMPTY
    })

    response = requests.request(POST, OES_LINE_PREP_URL, headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

########################################################################################

def submit_checkout_request(order_number, checkout_request_id, shipToCustomer, contact):
    payload = json.dumps({
        BILL_TO_CUSTOMER_ID: shipToCustomer.billToId,
        CONTACT_ID: contact.contactId,
        CONTACT_NAME: contact.contactName,
        CONTACT_EMAIL: contact.emailAddress,
        CONTACT_MOBILE: EMPTY,
        SHIP_TO_CUSTOMER_ID: shipToCustomer.customerId,
        SHIP_TO_NAME: shipToCustomer.customerName,
        SHIP_TO_ADD1: shipToCustomer.address.addressLine1,
        SHIP_TO_ADD2: shipToCustomer.address.addressLine2,
        SHIP_TO_CITY: shipToCustomer.address.city,
        SHIP_TO_STATE: shipToCustomer.address.state,
        SHIP_TO_POSTAL: shipToCustomer.address.zipCode,
        SHIP_TO_EXT: int(shipToCustomer.address.zipPlusFourCode),
        SHIP_TO_COUNTRY: shipToCustomer.address.countryCode,
        PAYMENT_TYPE: NET_30,
        TAX_OVERRIDE: True,
        SOURCE_APPLICATION: JOE_PHONE,
        SOURCE_CODE: FTWEB,
        MEXICO_USAGE_CODE: EMPTY,
        SUBMISSION_MODE: PARALLEL,
        KEEP_LOCKED: False
    })
    response = requests.request(POST, OES_SUBMIT_URL.format(order_number, checkout_request_id), headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

########################################################################################    

def add_lines(cr_id, num_qty_dict):
    for model, qty in num_qty_dict.items():
        line = line_preperation(model, qty)
        ext_prc = line[LINE][EXT_PRICE]
        item_id = line[LINE][ITEM_ID]
        
        # checkoutRequestId, itemId, quantity, extendedPrice (price of individual item)
        checkout_request = add_line(cr_id, item_id, qty, ext_prc)

    return checkout_request    

########################################################################################

def match_customer(pageable, address):
    content = pageable.content 
    for cust in content:
        if clean(cust.address.addressLine1) == clean(address[1]):
            if clean(cust.address.city) == clean(get_city(address[2])):
                if cust.address.zipCode == get_zipcode(address[2]):
                    if clean(cust.address.state) == clean(get_state(address[2])):
                        return cust

########################################################################################

def runner(model_number_qty_dict, bill_to, ship_to, contact):

    g2_order_number = get_order_number()
    uline_contact = search_contact(contact.name, contact.email)

    uline_shipto_pageable = search_customer(ship_to[1], get_city(ship_to[2]), uline_contact.customerName, get_zipcode(ship_to[2]), get_state(ship_to[2]))
    shipToCustomer = match_customer(uline_shipto_pageable, ship_to)

    checkout_request = create_checkout_request(g2_order_number, shipToCustomer, uline_contact)
    print(checkout_request)

    checkout_request_id = checkout_request.generalInfo.checkoutRequestId

    checkout_request = add_lines(checkout_request_id, model_number_qty_dict)  

    # Compute order summary and submit order
    checkout_request = compute_order_summary(checkout_request_id)
    checkout_request = submit_checkout_request(g2_order_number, checkout_request_id, shipToCustomer, uline_contact)
    print(checkout_request)
    
########################################################################################    
   