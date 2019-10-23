from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete SIP registration with id 1.

    SIP_REGISTRATION_ID = 1
    
    try:
        res = voxapi.delete_sip_registration(SIP_REGISTRATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
