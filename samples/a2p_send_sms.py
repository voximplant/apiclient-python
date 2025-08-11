from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Send the SMS message with the text "Test message" from the phone
    # number 447443332211 to the phone numbers 447443332212 and
    # 447443332213.

    SRC_NUMBER = "447443332211"
    DST_NUMBERS = ["447443332212", "447443332213"]
    TEXT = "Test message"
    
    try:
        res = voxapi.a2p_send_sms(SRC_NUMBER,
            DST_NUMBERS,
            TEXT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
