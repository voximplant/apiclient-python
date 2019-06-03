from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Enable the auto charging.

    AUTO_CHARGE = True
    PHONE_ID = 1
    
    res = voxapi.set_phone_number_info(AUTO_CHARGE, phone_id=PHONE_ID)
    print(res)
