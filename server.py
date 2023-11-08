from g2_gateway import *
from scraper.scraper import *

if __name__ == "__main__":
    order = parse_coupa_file("service/purchase_order.html")
    # print(search_customer("67 TAYLOR LN", "MINERAL BLUFF", "BEG TEXTILES", "30559", "GA").address.addressLine1)
    # print(search_contact("Robert Allen", "Robert.Allen@stericycle.com"))
    print(order)