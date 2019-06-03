from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all lists registered by user

    LIST_ID = 1
    OUTPUT = "json"
    
    res = voxapi.get_call_list_details(LIST_ID, output=OUTPUT)
    print(res)
