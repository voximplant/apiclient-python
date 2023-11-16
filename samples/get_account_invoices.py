from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # GetAccountInvoices example.

    
    try:
        res = voxapi.get_account_invoices()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
