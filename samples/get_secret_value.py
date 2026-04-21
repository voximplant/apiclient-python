from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the value of secret 10.

    APPLICATION_ID = 1
    SECRET_ID = 10
    
    try:
        res = voxapi.get_secret_value(application_id=APPLICATION_ID,
            secret_id=SECRET_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
