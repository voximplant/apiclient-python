from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the verification code.

    
    try:
        res = voxapi.verify_outbound_test_phone_number()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
