from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the admin user.

    REQUIRED_ADMIN_USER_ID = 1
    
    res = voxapi.del_admin_user(required_admin_user_id=REQUIRED_ADMIN_USER_ID)
    print(res)
