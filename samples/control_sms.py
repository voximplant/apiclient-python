from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Disable work with SMS for phone number 447443332211.

    PHONE_NUMBER = "447443332211"
    COMMAND = "disable"
    
    res = voxapi.control_sms(PHONE_NUMBER, COMMAND)
    print(res)
