from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all roles.

    
    try:
        res = voxapi.get_roles()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
