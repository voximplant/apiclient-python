from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Create SIP registration.

    SIP_USERNAME = "test"
    PROXY = "localhost"
    
    res = voxapi.create_sip_registration(SIP_USERNAME, PROXY)
    print(res)
