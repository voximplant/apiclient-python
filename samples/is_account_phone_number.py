from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Check if the phone number belongs to the account.

    PHONE_NUMBER = "79991234567"
    
    try:
        res = voxapi.is_account_phone_number(PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
