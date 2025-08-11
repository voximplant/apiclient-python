from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get two first identities.

    APPLICATION_ID = 1
    COUNT = 2
    
    try:
        res = voxapi.get_users(application_id=APPLICATION_ID,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
