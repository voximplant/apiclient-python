from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all lists registered by user.

    
    try:
        res = voxapi.get_call_lists()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
