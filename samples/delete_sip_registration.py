from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete SIP registration with id 1.

    SIP_REGISTRATION_ID = 1
    
    try:
        res = voxapi.delete_sip_registration(SIP_REGISTRATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
