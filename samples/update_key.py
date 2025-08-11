from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Create a new subuser for account_id = 1.

    KEY_ID = "ab98c70e-573e-4446-9af9-105269dfafca"
    DESCRIPTION = "test_desc"
    
    try:
        res = voxapi.update_key(KEY_ID,
            DESCRIPTION)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
