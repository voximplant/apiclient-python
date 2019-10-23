from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the admin user.

    REQUIRED_ADMIN_USER_ID = 1
    
    try:
        res = voxapi.del_admin_user(required_admin_user_id=REQUIRED_ADMIN_USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
