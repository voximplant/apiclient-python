from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Restore list with id = 1

    LIST_ID = 1
    
    try:
        res = voxapi.recover_call_list(LIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
