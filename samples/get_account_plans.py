from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get all account plans with packages.

    
    try:
        res = voxapi.get_account_plans()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
