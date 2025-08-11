from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Start the conference from the account.

    CONFERENCE_NAME = "boss"
    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    
    try:
        res = voxapi.start_conference(CONFERENCE_NAME,
            RULE_ID,
            script_custom_data=SCRIPT_CUSTOM_DATA)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
