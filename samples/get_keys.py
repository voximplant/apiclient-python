from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get keys info of the specified account.

    
    try:
        res = voxapi.get_keys()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
