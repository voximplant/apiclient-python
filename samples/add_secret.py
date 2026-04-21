from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new secret to application 1

    SECRET_NAME = "some_secret_name"
    SECRET_VALUE = "secret123"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_secret(SECRET_NAME,
            SECRET_VALUE,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
