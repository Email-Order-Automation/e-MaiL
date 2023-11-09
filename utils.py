import json
from collections import namedtuple
import aspose.pdf as ap
from http_params import *
import re
import win32com.client
import pickle

########################################################################################
 
def create_object(data):
    return json.loads(data, object_hook = lambda d : namedtuple('OBJECT', d.keys())(*d.values()))

########################################################################################

def generate_param(param, value):
    value = str(value)
    return "&" + param + "=" + value if value != "" else "" 

########################################################################################

def get_cust(name):
    if "," in name:
        return name.split(",")[0]
    return name    

########################################################################################

def get_city(location):
    return location.split(",")[0]

########################################################################################

def get_state(location):
    return location.split(" ")[1]

########################################################################################

def get_zipcode(location):
    location = location.split(" ")[2].strip()
    if "-" in location:
        return location.split("-")[0]
    return location    

########################################################################################

def clean(text):
    return ''.join(e for e in text if e.isalnum()).lower()

########################################################################################

def get_element_content(stringer):
    return re.sub(' +', ' ', stringer.get_text().strip().replace("\n", ""))

########################################################################################

def match_customer(pageable, address):
    content = pageable.content
    for cust in content:
        if clean(cust.address.addressLine1) == clean(address.get(ADDRESS_LINE1)):
            if clean(cust.address.city) == clean(address.get(CITY)):
                if cust.address.zipCode == address.get(ZIP):
                    if clean(cust.address.state) == clean(address.get(STATE)):
                        return cust

########################################################################################

def match_contact(name, email, pageable):
    content = pageable.content
    for contact in content:
        if contact.contactName.lower() == name.lower():
            if contact.emailAddress.lower() == email.lower():
                return contact                        
        
########################################################################################

def isNotEmpty(listy):
    return not len(listy) == 0

########################################################################################

def isValidIndex(idx):
    return idx != -1    

########################################################################################

def isHttpError(response):
    return hasattr(response, 'status') and hasattr(response, 'code') and hasattr(response, 'correlationId') and hasattr(response, 'message') and hasattr(response, 'developerMessage')

########################################################################################

def convert_pdf_to_html(attachment):
    document = ap.Document(attachment)
    save_options = ap.HtmlSaveOptions()
    document.save("C:\\Users\\Jacob.Powers\\Desktop\\eMaiL\\TEST.html", save_options)

########################################################################################

def get_emails():
    outlook=win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")

    inbox=outlook.GetDefaultFolder(6) 

    message=inbox.Items

    for m in message:
        if 'Purchase Order #' in m.Subject:
            # if 'coupahost.com' in m.Sender.GetExchangeUser().PrimarySmtpAddress:
            #     return m.Attachments
            if 'uline' in m.Sender.GetExchangeUser().PrimarySmtpAddress:
                attachment = m.Attachments.item(1)
                f=open('testorder.html', 'wb')
                f.write(attachment)
                f.close
                #attachment.SaveAsFile('C:\\Users\\Jacob.Powers\\Desktop\\eMaiL\\' + str(attachment))
                return f
                
            # if 'ansmtp.ariba.com' in m.Sender.GetExchangeUser().PrimarySmtpAddress:
            #     email_address = m.Sender.GetExchangeUser().PrimarySmtpAddress
            # else:
            #     return convert_pdf_to_html(m.attachment)