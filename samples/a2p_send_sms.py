from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Send the SMS message with the text "Test message" from the phone
    # number 447443332211 to the phone numbers 447443332212 and
    # 447443332213.

    SRC_NUMBER = "447443332211"
    DST_NUMBERS = "447443332212"
    TEXT = "Test message"
    
    try:
        res = voxapi.a2p_send_sms(SRC_NUMBER,
            DST_NUMBERS,
            TEXT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
