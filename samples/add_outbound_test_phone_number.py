from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add a personal phone number.

    PHONE_NUMBER = "12223334444"
    
    try:
        res = voxapi.add_outbound_test_phone_number(PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
