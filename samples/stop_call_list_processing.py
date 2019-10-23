from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Cancel list with id = 1

    LIST_ID = 1
    
    try:
        res = voxapi.stop_call_list_processing(LIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
