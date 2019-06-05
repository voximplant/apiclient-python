from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Enable the auto charging.

    AUTO_CHARGE = True
    PHONE_ID = 1
    
    try:
        res = voxapi.set_phone_number_info(AUTO_CHARGE, phone_id=PHONE_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
