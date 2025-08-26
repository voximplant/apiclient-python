from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # 

    WAB_PHONE_NUMBER = "12126367890"
    APPLICATION_ID = 1234
    RULE_ID = 5678
    
    try:
        res = voxapi.set_wab_phone_number_info(WAB_PHONE_NUMBER,
            application_id=APPLICATION_ID,
            rule_id=RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
