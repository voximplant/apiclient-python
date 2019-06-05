from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Unbind the user with id 123 from all SIP registrations.

    USER_ID = 123
    BIND = False
    
    try:
        res = voxapi.bind_sip_registration(user_id=USER_ID, bind=BIND)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
