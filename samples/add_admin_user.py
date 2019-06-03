from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new admin user.

    NEW_ADMIN_USER_NAME = "adm1"
    ADMIN_USER_DISPLAY_NAME = "adm1"
    NEW_ADMIN_USER_PASSWORD = "1234567"
    ADMIN_ROLE_ID = "1"
    
    res = voxapi.add_admin_user(NEW_ADMIN_USER_NAME, ADMIN_USER_DISPLAY_NAME, NEW_ADMIN_USER_PASSWORD, admin_role_id=ADMIN_ROLE_ID)
    print(res)
