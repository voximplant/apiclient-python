from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get two admin roles attached to the admin_user_id=22.

    WITH_ENTRIES = True
    SHOWING_ADMIN_USER_ID = 11
    INCLUDED_ADMIN_USER_ID = 22
    COUNT = 2
    
    try:
        res = voxapi.get_admin_roles(with_entries=WITH_ENTRIES, showing_admin_user_id=SHOWING_ADMIN_USER_ID, included_admin_user_id=INCLUDED_ADMIN_USER_ID, count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
