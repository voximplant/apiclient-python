from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Enable work with SMS for phone number 447443332211.

    PHONE_NUMBER = "447443332211"
    COMMAND = "enable"
    
    try:
        res = voxapi.control_sms(PHONE_NUMBER,
            COMMAND)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
