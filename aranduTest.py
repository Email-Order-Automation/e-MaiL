import win32com.client
from utils import *


def test():
    outlook=win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")

    inbox=outlook.GetDefaultFolder(6) 

    message=inbox.Items
    #message2=message.GetLast()
    #subject=message2.Subject
    #body=message2.body
    #date=message2.senton.date()
    #sender=message2.Sender
    #attachments=message2.Attachments

    # print(dir(inbox))

    for m in message:
        if 'Purchase Order #' in m.Subject:
            if 'coupahost.com' in m.Sender.GetExchangeUser().PrimarySmtpAddress:
                email_address = m.Sender.GetExchangeUser().PrimarySmtpAddress
                

            if 'ansmtp.ariba.com' in m.Sender.GetExchangeUser().PrimarySmtpAddress:
                email_address = m.Sender.GetExchangeUser().PrimarySmtpAddress
            else:
                # nothing
                print()
            print(email_address)



if __name__ == "__main__":
    # test()
    convert_pdf_to_html("C:\\Users\\Jacob.Powers\\Desktop\\eMaiL\\service\\TTM_Purchase_Order_2200101393.pdf")