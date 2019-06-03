from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Send the SMS message with text "Test message" from the phone number 447443332211 to the phone number 447443332212.

    SOURCE = "447443332211"
    DESTINATION = "447443332212"
    SMS_BODY = "Test message"
    
    res = voxapi.send_sms_message(SOURCE, DESTINATION, SMS_BODY)
    print(res)
