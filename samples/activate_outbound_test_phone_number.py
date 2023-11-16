from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Activate the personal phone number by the verification code.

    VERIFICATION_CODE = "12345"
    
    try:
        res = voxapi.activate_outbound_test_phone_number(VERIFICATION_CODE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
