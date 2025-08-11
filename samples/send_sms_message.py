from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Send the SMS message with the text "Test message" from the phone
    # number 447443332211 to the phone number 447443332212.

    SOURCE = "447443332211"
    DESTINATION = "447443332212"
    SMS_BODY = "Test message"
    
    try:
        res = voxapi.send_sms_message(SOURCE,
            DESTINATION,
            SMS_BODY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
