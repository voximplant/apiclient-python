from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # GetKeyValueItems example.

    KEY = "test"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_key_value_items(KEY,
            APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
