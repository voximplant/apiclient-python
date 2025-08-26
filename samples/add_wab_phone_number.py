from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Adds a new WhatsApp Business phone number.

    WAB_PHONE_NUMBER = "12126367890"
    VOICE_PASSWORD = "abc"
    
    try:
        res = voxapi.add_wab_phone_number(WAB_PHONE_NUMBER,
            VOICE_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
