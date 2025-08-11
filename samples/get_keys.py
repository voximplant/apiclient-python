from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get keys info of the specified account.

    
    try:
        res = voxapi.get_keys()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
