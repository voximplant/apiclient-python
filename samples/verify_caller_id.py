from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Verify the callerID 1.

    CALLERID_ID = 1
    
    try:
        res = voxapi.verify_caller_id(callerid_id=CALLERID_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
