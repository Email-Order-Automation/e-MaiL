POST = "POST"
GET = "GET"
PUT = "PUT"
DELETE = "DELETE"

SECURITY_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:31114/security-services/v3"
SECURITY_AUTH_URL = SECURITY_BASE_URL + "/auth"

OES_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11378/order-entry-service/v1"
OES_LINES_URL = OES_BASE_URL + "/checkout-requests/{0}/lines"
OES_CHECKOUT_REQ_URL = OES_BASE_URL + "/checkout-requests"
OES_LINE_PREP_URL = OES_BASE_URL + "/orders/line-preparation"
OES_SUBMIT_URL = OES_BASE_URL + "/orders/{0}/submit-checkout-request/{1}"
OES_SUMMARY_URL = OES_BASE_URL + "/checkout-requests/{0}/summary"

ORDER_BASE_URL = "http://dc2-svzgsys03.ulinedm.com:11174/order-service/v1"
ORDER_NUMBER_URL = ORDER_BASE_URL + "/orders/order-number"
GET_ORDER_URL = ORDER_BASE_URL + "/orders/{0}"

ITEM_SERVICE_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:21102/item-services/v2"

CUSTOMER_SERVICE_BASE_URL = "http://dc2-svzgsys01.ulinedm.com:11394/customer-service/v1"
CUSTOMER_SEARCH_URL = CUSTOMER_SERVICE_BASE_URL + "/customers/search?"
CONTACT_SEARCH_URL = CUSTOMER_SERVICE_BASE_URL + "/contacts/search?"
BILL_TO_URL = CUSTOMER_SERVICE_BASE_URL + "/bill-tos"

LOCATION_SERVICE_BASE_URL = "http://dc2-svzgsys05.ulinedm.com:21156/location-services/v2"

ORDER_INTEGRATION_SERVICE_BASE_URL = "http://dc2-svzgsys07.ulinedm.com:11288/order-integration-service/v1"
LEGACY_INTEGRATION_URL = ORDER_INTEGRATION_SERVICE_BASE_URL + "/legacy-integration"