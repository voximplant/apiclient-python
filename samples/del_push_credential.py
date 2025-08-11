from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Remove credentials.

    PUSH_CREDENTIAL_ID = 1
    
    try:
        res = voxapi.del_push_credential(PUSH_CREDENTIAL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
