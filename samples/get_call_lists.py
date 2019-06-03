from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all lists registered by user

    
    res = voxapi.get_call_lists()
    print(res)
