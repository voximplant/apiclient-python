from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get subuser's roles.

    SUBUSER_ID = 12
    
    try:
        res = voxapi.get_sub_user_roles(SUBUSER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
