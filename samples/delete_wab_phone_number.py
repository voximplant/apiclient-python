from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Deletes a WhatsApp Business phone number.

    WAB_PHONE_NUMBER = "12126367890"
    
    try:
        res = voxapi.delete_wab_phone_number(WAB_PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
