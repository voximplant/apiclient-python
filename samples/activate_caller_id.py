from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Activate the callerID by the verification code.

    VERIFICATION_CODE = "12345"
    CALLERID_ID = 1
    
    try:
        res = voxapi.activate_caller_id(VERIFICATION_CODE,
            callerid_id=CALLERID_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
