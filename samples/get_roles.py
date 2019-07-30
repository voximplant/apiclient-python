from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all roles.

    
    try:
        res = voxapi.get_roles()
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
