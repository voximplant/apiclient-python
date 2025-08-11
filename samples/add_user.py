from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new user.

    USER_NAME = "GordonFreeman"
    USER_DISPLAY_NAME = "GordonFreeman"
    USER_PASSWORD = "1234567"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_user(USER_NAME,
            USER_DISPLAY_NAME,
            USER_PASSWORD,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
