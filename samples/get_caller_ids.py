from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the two callerIDs.

    COUNT = 2
    
    try:
        res = voxapi.get_caller_ids(count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
