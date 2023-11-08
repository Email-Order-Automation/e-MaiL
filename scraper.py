from bs4 import BeautifulSoup
from enum import Enum


# coupa html files
with open("purchase_order.html", encoding="utf8") as fp:
    order = BeautifulSoup(fp, "html.parser")

    lines = order.find(id="order_lines").find_all('tr')
    
    for line in lines:

        fields = line.find_all('td')



        for field in fields:
            print(field)
            print("mmmmmgatorade")


function map_fields_to_item()

class Rows(Enum):
    LINE_NUM = 1
    DESCRIPTION = 2
    NBD = 3
    QTY = 4
    UNIT = 5
    PRICE = 6
    TOTAL = 7