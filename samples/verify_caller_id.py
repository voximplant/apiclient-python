from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Verify the callerID 1.

    CALLERID_ID = 1
    
    res = voxapi.verify_caller_id(callerid_id=CALLERID_ID)
    print(res)
