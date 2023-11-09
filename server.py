from g2_gateway import *
from scrapper.scrapper import *

if __name__ == "__main__":
    with open("service/purchase_order.html", encoding="utf8") as fp:
        order = parse_coupa_file(fp)
    customer = search_customer(order.ship_to[1], get_city(order.ship_to[2]), order.ship_to[0], get_zipcode(order.ship_to[2]), get_state(order.ship_to[2]))
    print(customer)