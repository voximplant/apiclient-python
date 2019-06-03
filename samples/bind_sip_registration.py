from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Unbind the user with id 123 from all SIP registrations.

    USER_ID = 123
    BIND = False
    
    res = voxapi.bind_sip_registration(user_id=USER_ID, bind=BIND)
    print(res)
