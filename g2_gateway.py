import requests
import json
from urllib.parse import urlencode
from urllib.request import urlretrieve

OES_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11378/order-entry-service/v1"
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

def create_checkout_request():
    url = OES_BASE_URL + "/checkout-requests"

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
        "orderNumber": 90114059
    })

    response = requests.request("POST", url, headers=STANDARD_HEADERS, data=payload)
    return json.loads(response.text)

def search_customer(address_line, city, customer_name, postal_code, state_province_code):
    url = CUSTOMER_SERVICE_BASE_URL + "/customers/search?"
    generate_param("addressLine", address_line)
    generate_param("city", city)
    generate_param("postalCode", customer_name)
    generate_param("postalCode", postal_code)
    if address_line != "":
        url += "addressLine=" + address_line
    if city != "":
        url += "&city=" + city
    if customer_name != "":
        url += "&customerName=" + customer_name
    if postal_code != "":
        url += "&postalCode=" + postal_code
    if state_province_code != "":
        url += "&stateProvinceCode=" + state_province_code
    response = requests.request("GET", url, headers=STANDARD_HEADERS)
    return json.loads(response.text)

def search_customer_by_address(address_line, size):
    url = CUSTOMER_SERVICE_BASE_URL + "/customers/search?"
    if address_line != "":
        url += "addressLine=" + address_line
    if size != "":
        url += "&size=" + size
    response = requests.request("GET", url, headers=STANDARD_HEADERS)
    return json.loads(response.text)

def get_countries():
    url = LOCATION_SERVICE_BASE_URL + "/countries"
    response = requests.request("GET", url, headers=STANDARD_HEADERS)
    return json.loads(response.text)
    

def add_line(checkout_request_id, item_id, quantity, extended_price):

    url = "{0}/checkout-requests/{1}/lines".format(OES_BASE_URL, checkout_request_id)

    payload = json.dumps({
          "lines": [
        {
            "itemId": str(item_id),
            "productId": None,
            "sellableOrderedQuantity": int(quantity),
            "extendedPrice": float(extended_price),
            "raCode": ""
        }]
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


def runner(model_number_qty_dict):
    # Create checkout request
    checkout_request = create_checkout_request()
    checkout_request_id = checkout_request["generalInfo"]["checkoutRequestId"]

    # Iterate through item numbers and add to order
    for model_number, quantity in model_number_qty_dict.items():
        prepared_line = line_preperation(model_number, quantity)
        # print(prepared_line)
        extended_price = prepared_line["line"]["extendedPrice"]
        item_id = prepared_line["line"]
        
        # checkoutRequestId, itemId, quantity, extendedPrice (price of individual item)
        checkout_request = add_line(checkout_request_id, item_id, quantity, extended_price)
        print(checkout_request)
        # print(checkout_request)
    
    # Compute order summary and submit order
    checkout_request = compute_order_summary(checkout_request_id)
    print(checkout_request)
    


if __name__ == "__main__":
    runner({"H-101":1, "S-8080":25})

   