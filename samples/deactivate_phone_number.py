from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Deactivate the phone 1.

    PHONE_ID = 1
    
    try:
        res = voxapi.deactivate_phone_number(phone_id=PHONE_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
