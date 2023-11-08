import sys
sys.path.append("..\scraper")
from scraper import parse_coupa_file
sys.path.append("..")
from g2_gateway import runner 

def get_uline_item_number(desc):
    h_item_idx = desc.find("H-")
    s_item_idx = desc.find("S-")

    if h_item_idx != -1:
        end_idx = desc[h_item_idx:].find(" ")
        if end_idx != -1:
            return desc[h_item_idx:end_idx]

        return desc[h_item_idx:]  

    if s_item_idx != -1:
        end_idx = desc[s_item_idx:].find(" ")
        if end_idx != -1:
            return desc[s_item_idx:end_idx]

        return desc[s_item_idx:]
        
def build_line_item():
    with open("purchase_order.html", encoding="utf8") as fp:
        items = parse_coupa_file(fp)

        req = {}
        for item in items:
            req[get_uline_item_number(item.description)] = int(item.quantity)
            print(req)

        runner(req)    


build_line_item()