from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Edit the user password.

    USER_ID = 1
    USER_PASSWORD = "7654321"
    
    try:
        res = voxapi.set_user_info(user_id=USER_ID,
            user_password=USER_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
