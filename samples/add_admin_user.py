from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new admin user.

    NEW_ADMIN_USER_NAME = "Overseer_Campbell"
    ADMIN_USER_DISPLAY_NAME = "Overseer_Campbell"
    NEW_ADMIN_USER_PASSWORD = "1234567"
    ADMIN_ROLE_ID = "1"
    
    try:
        res = voxapi.add_admin_user(NEW_ADMIN_USER_NAME,
            ADMIN_USER_DISPLAY_NAME,
            NEW_ADMIN_USER_PASSWORD,
            admin_role_id=ADMIN_ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
