from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind the all admin users with the admin roles 1, 2 and 3.

    REQUIRED_ADMIN_USER_ID = "all"
    ADMIN_ROLE_ID = [1, 2, 3]
    
    res = voxapi.attach_admin_role(required_admin_user_id=REQUIRED_ADMIN_USER_ID, admin_role_id=ADMIN_ROLE_ID)
    print(res)
