import json
from collections import namedtuple
 
def create_object(data):
    return json.loads(data, object_hook = lambda d : namedtuple('OBJECT', d.keys())(*d.values()))

def generate_param(param, value):
    return "&" + param + "=" + value if value != "" else "" 