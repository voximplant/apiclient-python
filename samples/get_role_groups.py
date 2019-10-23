from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all role groups.

    
    try:
        res = voxapi.get_role_groups()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
