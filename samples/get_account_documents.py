from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    WITH_DETAILS = True
    
    try:
        res = voxapi.get_account_documents(with_details=WITH_DETAILS)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
