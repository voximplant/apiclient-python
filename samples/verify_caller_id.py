from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Verify the callerID 1.

    CALLERID_ID = 1
    
    try:
        res = voxapi.verify_caller_id(callerid_id=CALLERID_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
