from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Restore list with id = 1

    LIST_ID = 1
    
    res = voxapi.recover_call_list(LIST_ID)
    print(res)
