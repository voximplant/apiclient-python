from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get push credentials.

    DIALOGFLOW_KEY_ID = 1
    
    try:
        res = voxapi.get_dialogflow_keys(dialogflow_key_id=DIALOGFLOW_KEY_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
