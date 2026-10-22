from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Start the scripts from the account.

    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    
    try:
        res = voxapi.start_scenarios(rule_id=RULE_ID,
            script_custom_data=SCRIPT_CUSTOM_DATA)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
