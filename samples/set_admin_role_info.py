from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Allow the all permissions except the DelUser and DelApplication.

    ADMIN_ROLE_ID = 1
    ENTRY_MODIFICATION_MODE = "set"
    ALLOWED_ENTRIES = "all"
    DENIED_ENTRIES = ["DelUser", "DelApplication"]
    
    try:
        res = voxapi.set_admin_role_info(admin_role_id=ADMIN_ROLE_ID,
            entry_modification_mode=ENTRY_MODIFICATION_MODE,
            allowed_entries=ALLOWED_ENTRIES,
            denied_entries=DENIED_ENTRIES)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
