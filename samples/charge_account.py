from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Charge the frozen phone number: 79993330011.

    PHONE_NUMBER = "79993330011"
    
    try:
        res = voxapi.charge_account(phone_number=PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
