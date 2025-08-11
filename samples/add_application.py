from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new application.

    APPLICATION_NAME = "myapp1"
    
    try:
        res = voxapi.add_application(APPLICATION_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
