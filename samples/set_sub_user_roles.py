from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add the roles 1, 2, 3 to the subuser with id = 12.

    SUBUSER_ID = 12
    ROLE_ID = [1, 2, 3]
    
    try:
        res = voxapi.set_sub_user_roles(SUBUSER_ID,
            role_id=ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
