from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Deactivate the phone 1.

    PHONE_ID = 1
    
    res = voxapi.deactivate_phone_number(phone_id=PHONE_ID)
    print(res)
