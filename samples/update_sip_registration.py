from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind SIP registration with id 1 to the application with id 123.

    SIP_REGISTRATION_ID = 1
    APPLICATION_ID = 123
    
    res = voxapi.update_sip_registration(SIP_REGISTRATION_ID, application_id=APPLICATION_ID)
    print(res)
