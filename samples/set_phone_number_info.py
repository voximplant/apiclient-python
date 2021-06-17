from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Enable the auto charging.

    PHONE_ID = 1
    
    try:
        res = voxapi.set_phone_number_info(phone_id=PHONE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
