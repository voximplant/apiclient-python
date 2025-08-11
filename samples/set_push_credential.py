from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Modify credentials.

    PUSH_CREDENTIAL_ID = 1
    CERT_PASSWORD = "1234567"
    
    try:
        res = voxapi.set_push_credential(PUSH_CREDENTIAL_ID,
            cert_password=CERT_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
