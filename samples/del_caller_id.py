from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the callerID 1.

    CALLERID_ID = 1
    
    try:
        res = voxapi.del_caller_id(callerid_id=CALLERID_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
