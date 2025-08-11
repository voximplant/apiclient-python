from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get push credentials.

    PUSH_CREDENTIAL_ID = 1
    
    try:
        res = voxapi.get_push_credential(push_credential_id=PUSH_CREDENTIAL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
