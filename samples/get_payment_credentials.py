from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Gets the saved credit cards.

    
    try:
        res = voxapi.get_payment_credentials()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
