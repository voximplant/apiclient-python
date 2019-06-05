from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Edit the admin user password.

    REQUIRED_ADMIN_USER_ID = 1
    NEW_ADMIN_USER_PASSWORD = "7654321"
    
    try:
        res = voxapi.set_admin_user_info(required_admin_user_id=REQUIRED_ADMIN_USER_ID, new_admin_user_password=NEW_ADMIN_USER_PASSWORD)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
