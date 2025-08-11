from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Create SIP registration.

    SIP_USERNAME = "JohnGalt"
    PROXY = "localhost"
    
    try:
        res = voxapi.create_sip_registration(SIP_USERNAME,
            PROXY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
