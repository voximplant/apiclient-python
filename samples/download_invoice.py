from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Download the invoice with id = 1.

    INVOICE_ID = 1
    
    try:
        res = voxapi.download_invoice(INVOICE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
