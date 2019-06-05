from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Disable work with SMS for phone number 447443332211.

    PHONE_NUMBER = "447443332211"
    COMMAND = "disable"
    
    try:
        res = voxapi.control_sms(PHONE_NUMBER, COMMAND)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
