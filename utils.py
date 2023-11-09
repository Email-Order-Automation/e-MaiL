import json
from collections import namedtuple
 
def create_object(data):
    return json.loads(data, object_hook = lambda d : namedtuple('OBJECT', d.keys())(*d.values()))

def generate_param(param, value):
    value = str(value)
    return "&" + param + "=" + value if value != "" else "" 

def get_cust(name):
    if "," in name:
        return name.split(",")[0]
    return name    

def get_city(location):
    return location.split(",")[0]

def get_state(location):
    return location.split(" ")[1]

def get_zipcode(location):
    location = location.split(" ")[2].strip()
    if "-" in location:
        return location.split("-")[0]
    return location    

def clean(text):
    return ''.join(e for e in text if e.isalnum()).lower()   