from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get roles of the key.

    KEY_ID = "ab81c50e-573e-4446-9af9-105269dfafca"
    
    try:
        res = voxapi.get_key_roles(KEY_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
