from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Charge the all frozen phone numbers.

    PHONE_NUMBER = "all"
    
    res = voxapi.charge_account(phone_number=PHONE_NUMBER)
    print(res)
