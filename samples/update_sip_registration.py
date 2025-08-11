from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Update SIP registration with id 1.

    SIP_REGISTRATION_ID = 1
    SIP_USERNAME = "HedyLamarr"
    OUTBOUND_PROXY = "12"
    PASSWORD = "123456"
    
    try:
        res = voxapi.update_sip_registration(SIP_REGISTRATION_ID,
            sip_username=SIP_USERNAME,
            outbound_proxy=OUTBOUND_PROXY,
            password=PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
