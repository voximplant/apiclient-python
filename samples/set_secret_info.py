from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Update the value for secret 10.

    APPLICATION_ID = 1
    SECRET_ID = 10
    SECRET_VALUE = "newsecret456"
    
    try:
        res = voxapi.set_secret_info(application_id=APPLICATION_ID,
            secret_id=SECRET_ID,
            secret_value=SECRET_VALUE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
