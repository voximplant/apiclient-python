from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get two first admin users.

    WITH_ACCESS_ENTRIES = True
    COUNT = 2
    
    try:
        res = voxapi.get_admin_users(with_access_entries=WITH_ACCESS_ENTRIES, count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
