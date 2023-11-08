import requests
import json

OES_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11378/order-entry-service/v1"
ITEM_SERVICE_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:21102/item-services/v2"
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


def create_checkout_request():
    url = OES_BASE_URL + "/checkout-requests"

    payload = json.dumps({
        "companyCode": "UL-US",
        "catalogCode": "FV",
        "sourceApplication": "JOE-PHONE",
        "orderType": "PHONE_ORDER",
        "prioritySourceCode": "",
        "customerPurchaseOrderNumber": "SH_072522001",
        "finderSourceCode": "",
        "keepLocked": False,
        "mexicoUsageCode": "P01",
        "billToCustomerId": 28676096,
        "shipToCustomerId": 28676098,
        "contactId": 18263813,
        "orderNumber": 90114059
    })
    headers = {
        'Content-': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ULINE_TOKEN
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

def add_line(checkout_request_id):

    url = OES_BASE_URL + f"/checkout-requests/{0}/lines".format(checkout_request_id)

    payload = json.dumps({
    "lines": [
        {
        "itemId": 26323,
        "productId": None,
        "sellableOrderedQuantity": 10,
        "extendedPrice": 130,
        "raCode": ""
        }
    ]
    })
    headers = {
    'Content-': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ULINE_TOKEN
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

ULINE_TOKEN = get_uline_token()
checkout_request = create_checkout_request()