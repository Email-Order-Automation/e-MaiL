import requests
import json
from urllib.parse import urlencode
from urllib.request import urlretrieve
from utils import *

OES_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11378/order-entry-service/v1"
ORDER_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11174/order-service/v1"
ITEM_SERVICE_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:21102/item-services/v2"
CUSTOMER_SERVICE_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:11394/customer-service/v1"
LOCATION_SERVICE_BASE_URL = "http://dc2-svzgsys05.ulinedm.com:21156/location-services/v2"
ULINE_TOKEN = ""


def get_uline_token():
    url = "http://dc2-svzgsys01.ulinedm.com:31114/security-services/v3/auth"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic cGVyZm9ybTU6VWxpbmUxMjM='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_data = json.loads(response.text)
    return(json_data["token"])

ULINE_TOKEN = get_uline_token()
STANDARD_HEADERS = {
        'Content-': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ULINE_TOKEN
    }

def get_order_number():
    response = requests.request("POST", ORDER_BASE_URL + "/orders/order-number", headers=STANDARD_HEADERS, data="{}")
    return json.loads(response.text)

def create_checkout_request(order_number):
    payload = json.dumps({
        "companyCode": "UL-US",
        "catalogCode": "FV",
        "sourceApplication": "JOE-PHONE",
        "orderType": "PHONE_ORDER",
        "prioritySourceCode": "",
        "customerPurchaseOrderNumber": "G2",
        "finderSourceCode": "",
        "keepLocked": False,
        "mexicoUsageCode": "P01",
        "billToCustomerId": 28676096,
        "shipToCustomerId": 28676098,
        "contactId": 18263813,
        "orderNumber": order_number["orderNumber"]
    })

    response = requests.request("POST", OES_BASE_URL + "/checkout-requests", headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

def search_customer(address_line, city, customer_name, postal_code, state_province_code):
    url = CUSTOMER_SERVICE_BASE_URL + "/customers/search?"
    url += generate_param("addressLine", address_line)
    url += generate_param("city", city)
    url += generate_param("customerName", customer_name)
    url += generate_param("postalCode", postal_code)
    url += generate_param("stateProvinceCode", state_province_code)
    response = requests.request("GET", url, headers=STANDARD_HEADERS)
    return create_object(response.text).content[0]
    
def search_contact(name, emailAddress):
    url = CUSTOMER_SERVICE_BASE_URL + "/contacts/search?"
    url += generate_param("name", name)
    url += generate_param("emailAddress", emailAddress)
    response = requests.request("GET", url, headers=STANDARD_HEADERS)
    return create_object(response.text).content[0]
    

def add_line(checkout_request_id, item_id, quantity, extended_price):

    url = "{0}/checkout-requests/{1}/lines".format(OES_BASE_URL, checkout_request_id)
    payload = json.dumps({
        "lines": [
            {
            "itemId": item_id,
            "productId": None,
            "sellableOrderedQuantity": quantity,
            "extendedPrice": extended_price,
            "raCode": ""
            }
        ]
        })

    response = requests.request("POST", url, headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

def compute_order_summary(checkout_request_id):
    url = "{0}/checkout-requests/{1}/summary".format(OES_BASE_URL, checkout_request_id)
    response = requests.request("POST", url, headers=STANDARD_HEADERS, data="{}")
    return json.loads(response.text)

def line_preperation(model_number, quantity):
    payload = json.dumps({
        "companyCode" : "UL-US",
        "modelNumber" : model_number,
        "quantity" : quantity,
        "raCode" : ""
    })
    response = requests.request("POST", OES_BASE_URL + "/orders/line-preparation", headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

def submit_checkout_request(order_number, checkout_request_id):
    payload = json.dumps({
        "billToCustomerId": "28676096",
        "contactId": "18263813",
        "contactName": "RACHAEL COMSTOCK",
        "contactEmailAddress": "RCOMSTOCK1@YAHOO.COM",
        "contactMobileNumber": "",
        "shipToCustomerId": "28676098",
        "shipToCustomerName": "RACHAEL COMSTOCK",
        "shipToAddress1": "1240 22ND AVE",
        "shipToAddress2": "",
        "shipToCity": "KENOSHA",
        "shipToStateProvinceCode": "WI",
        "shipToPostalCode": "53140",
        "shipToPostalCodeExtension": "4304",
        "shipToCountryCode": "US",
        "paymentTypeCode": "NET_30",
        "taxOverridden": True,
        "sourceApplication": "JOE-PHONE",
        "selectedSourceCode": "FTWEB",
        "mexicoUsageCode": "",
        "submissionMode": "PARALLEL",
        "keepLocked": False
    })
    
    response = requests.request("POST", "{0}/orders/{1}/submit-checkout-request/{1}".format(OES_BASE_URL, order_number, checkout_request_id), headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)


def runner(model_number_qty_dict):
    # Create checkout request
    order_number = get_order_number()
    print(order_number)
    checkout_request = create_checkout_request(order_number)
    print(checkout_request)
    checkout_request_id = checkout_request["generalInfo"]["checkoutRequestId"]

    # Iterate through item numbers and add to order
    for model_number, quantity in model_number_qty_dict.items():
        prepared_line = line_preperation(model_number, quantity)
        extended_price = prepared_line["line"]["extendedPrice"]
        item_id = prepared_line["line"]["itemId"]
        
        # checkoutRequestId, itemId, quantity, extendedPrice (price of individual item)
        checkout_request = add_line(checkout_request_id, item_id, quantity, extended_price)
    
    # Compute order summary and submit order
    checkout_request = compute_order_summary(checkout_request_id)
    checkout_request = submit_checkout_request(order_number, checkout_request_id)
    print(checkout_request)
    


if __name__ == "__main__":
    runner({"H-101":1, "S-8080":25})

   