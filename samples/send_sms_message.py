from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Send the SMS message with text "Test message" from the phone number 447443332211 to the phone number 447443332212.

    SOURCE = "447443332211"
    DESTINATION = "447443332212"
    SMS_BODY = "Test message"
    
    try:
        res = voxapi.send_sms_message(SOURCE, DESTINATION, SMS_BODY)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
