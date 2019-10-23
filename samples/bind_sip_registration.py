from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind SIP registration with id 1 to application with id 123.

    APPLICATION_ID = 123
    SIP_REGISTRATION_ID = 1
    BIND = True
    
    try:
        res = voxapi.bind_sip_registration(application_id=APPLICATION_ID,
            sip_registration_id=SIP_REGISTRATION_ID,
            bind=BIND)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
