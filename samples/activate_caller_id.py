from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Activate the callerID by the verification code.

    VERIFICATION_CODE = "12345"
    CALLERID_ID = 1
    
    try:
        res = voxapi.activate_caller_id(VERIFICATION_CODE, callerid_id=CALLERID_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
