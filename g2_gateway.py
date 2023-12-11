import requests
import json
import time
from client_urls import *
from http_params import *
from urllib.parse import urlencode
from urllib.request import urlretrieve
from uline_utils import *

########################################################################################

def get_uline_token():
    headers = {
        CONTENT_TYPE: APPLICATION_JSON,
        AUTHORIZATION: BASIC
    }

    response = requests.request(POST, SECURITY_AUTH_URL, headers=headers, data=EMPTY)

    obj = create_object(response.text)

    if isHttpError(obj): 
        raise ConnectionError("Error getting bearer token")
    else: return obj.token
    

########################################################################################

STANDARD_HEADERS = {
        CONTENT_TYPE: APPLICATION_JSON,
        AUTHORIZATION: BEARER + " " + get_uline_token()
    }

########################################################################################

def get_order_number():
    response = requests.request(POST, ORDER_NUMBER_URL, headers=STANDARD_HEADERS, data="{}")
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Error getting new order number from order service")
    else: return obj.orderNumber #+ FIVE_BILLION

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
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Error creating checkout request for order number: " + str(order_number) + " and customer ID: " + str(shipToCustomer.customerId))
    else: return obj

########################################################################################    

def search_customer(address):
    url = CUSTOMER_SEARCH_URL
    url += generate_param(ADDRESS_LINE, address.get(ADDRESS_LINE1))
    url += generate_param(CITY, address.get(CITY))
    url += generate_param(POSTAL_CODE, address.get(ZIP))
    url += generate_param(STATE_PROV_CODE, address.get(STATE))
    url += generate_param(MARKED_DEL, False)
    url_with_customer_name = url + generate_param(CUSTOMER_NAME, address.get(CUSTOMER_NAME))
    
    response = requests.request(GET, url, headers=STANDARD_HEADERS)
    obj = create_object(response.text)
    
    if isHttpError(obj):
        raise ConnectionError("Error in customer search")
    if(obj.numberOfElements <= 1):
        return obj
    
    response = requests.request(GET, url_with_customer_name, headers=STANDARD_HEADERS)
    obj = create_object(response.text)
    
    if isHttpError(obj):
        raise ConnectionError("Error in customer search")
    return obj


######################################################################################## 
    
def search_contact(name, email):
    url = CONTACT_SEARCH_URL
    url += generate_param(NAME, name)
    url += generate_param(EMAIL, email)
    url += generate_param(CUST_MARKED_DEL, False)

    response = requests.request(GET, url, headers=STANDARD_HEADERS)
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Error in contact search")    
    else: return match_contact(name, email, obj)
    
########################################################################################

def add_line(cr_id, item_id, qty, ext_price):
    payload = json.dumps({
        LINES: [
            {
            ITEM_ID: item_id,
            PRODUCT_ID: None,
            SELLABLE_ORDERED_QTY: qty,
            EXT_PRICE: ext_price,
            RA_CODE: EMPTY
            }
        ]
        })

    response = requests.request(POST, OES_LINES_URL.format(cr_id), headers=STANDARD_HEADERS, data=payload)
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Error adding order line to checkout request: " + str(cr_id))
    else: return obj

########################################################################################    

def compute_order_summary(cr_id):
    response = requests.request(POST, OES_SUMMARY_URL.format(cr_id), headers=STANDARD_HEADERS, data="{}")
    obj = create_object(response.text)

    if isHttpError(obj): 
        raise ConnectionError("Error computing order summary for checkout request: " + str(cr_id))
    else: return obj

########################################################################################

def line_preperation(model_number, quantity):
    payload = json.dumps({
        COMPANY_CODE : US_COMP_CODE,
        MODEL_NUM : model_number,
        QTY : quantity,
        RA_CODE : EMPTY
    })
    response = requests.request(POST, OES_LINE_PREP_URL, headers=STANDARD_HEADERS, data=payload)
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Error preparing line information for model number: " + str(model_number))
    else: return obj

########################################################################################

def submit_checkout_request(order_number, cr_id, shipToCustomer, contact):
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
        SUBMISSION_MODE: PRIMARY,
        KEEP_LOCKED: False
    })
    
    response = requests.request(POST, OES_SUBMIT_URL.format(order_number, cr_id), headers=STANDARD_HEADERS, data=payload)
    
    if(response.status_code > 200):
        raise ConnectionError("Error submitting checkout request: " + str(cr_id) + " with order number: " + str(order_number))

    return create_object(response.text)
        
    

########################################################################################

def integrate_order(order_number):
    payload = json.dumps({
        ORDER_NUMBER: order_number
    })
    num_tries = 0

    while num_tries < 5:
        response = requests.request(POST, LEGACY_INTEGRATION_URL, headers=STANDARD_HEADERS, data=payload)
        order_response = get_order_response(order_number, SOURCED_FROM_DSE_ARG)
        order_status = order_response.orderStatus
        if(order_status == ON_HOLD_INTEGRATED_STATUS or order_status == NEW_ORDER_STATUS):
            break
        num_tries += 1
    
    obj = create_object(response.text)

    if isHttpError(obj):
        return False
    else: return True

########################################################################################

def wait_for_order_on_hold_pending_integration_or_new_order(order_number):
    
    num_checks = 0
    order_status = None
    time.sleep(10)
    if(order_status == ON_HOLD_PENDING_INTEGRATION_STATUS or order_status == NEW_ORDER_STATUS):
            return order_status
    while num_checks < 8:
        order_response = get_order_response(order_number, SOURCED_FROM_DSE_ARG)
        order_status = order_response.orderStatus
        num_checks += 1
        run_hold_check(order_number)
        if(order_status == ON_HOLD_PENDING_INTEGRATION_STATUS or order_status == NEW_ORDER_STATUS):
            return order_status
        time.sleep(5)
    if(order_status == PENDING_SUBMIT_POST_PROCESSING_STATUS):
        raise ConnectionError("Order " + str(order_number) + " stuck in post processing")
    else:
        raise ConnectionError("Order " + str(order_number) + " stuck in processing")
    


########################################################################################

def get_order_response(order_number, sourced_from):
    
    url = GET_ORDER_URL + "?"
    url += generate_param(SOURCED_FROM_PARAM, sourced_from)
    url = url.format(order_number)
    
    response = requests.request(GET, url, headers=STANDARD_HEADERS, data="{}")
    obj = create_object(response.text)

    if isHttpError(obj):
        raise ConnectionError("Unable to get order with order number " + str(order_number))
    else: return obj

########################################################################################

def run_hold_check(order_number):
    
    url = RUN_HOLD_CHECK_URL
    url = url.format(order_number)
    payload = json.dumps({
        SOURCE_APPLICATION_PARAM: HOQ_SOURCE_APPLICATION_PARAM
    })
    
    requests.request(POST, url, headers=STANDARD_HEADERS, data=payload)

########################################################################################