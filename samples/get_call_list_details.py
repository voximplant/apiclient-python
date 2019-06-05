from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all lists registered by user

    LIST_ID = 1
    OUTPUT = "json"
    
    try:
        res = voxapi.get_call_list_details(LIST_ID, output=OUTPUT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
