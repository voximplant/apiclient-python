from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Charge the all frozen phone numbers.

    PHONE_NUMBER = "all"
    
    try:
        res = voxapi.charge_account(phone_number=PHONE_NUMBER)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
