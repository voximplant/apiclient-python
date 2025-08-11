from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Create a key pair.

    
    try:
        res = voxapi.create_key()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
