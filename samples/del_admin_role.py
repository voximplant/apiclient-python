from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the admin role.

    ADMIN_ROLE_ID = 10
    
    res = voxapi.del_admin_role(admin_role_id=ADMIN_ROLE_ID)
    print(res)
