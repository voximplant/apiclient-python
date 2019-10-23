from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all record storages.

    
    try:
        res = voxapi.get_record_storages()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
