from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the all available admin role entries.

    
    try:
        res = voxapi.get_available_admin_role_entries()
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
