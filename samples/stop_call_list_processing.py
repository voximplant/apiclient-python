from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Cancel list with id = 1

    LIST_ID = 1
    
    res = voxapi.stop_call_list_processing(LIST_ID)
    print(res)
