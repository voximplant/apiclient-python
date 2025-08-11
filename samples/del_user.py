from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete two users with ID 3 and 55.

    USER_ID = [3, 55]
    
    try:
        res = voxapi.del_user(user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
