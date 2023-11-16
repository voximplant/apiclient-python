from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the phone number info.

    
    try:
        res = voxapi.get_outbound_test_phone_numbers()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
