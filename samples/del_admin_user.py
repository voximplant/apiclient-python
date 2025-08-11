from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete the admin user.

    REQUIRED_ADMIN_USER_ID = 1
    
    try:
        res = voxapi.del_admin_user(required_admin_user_id=REQUIRED_ADMIN_USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
