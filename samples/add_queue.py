from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new ACD queue for the application 1.

    ACD_QUEUE_NAME = "myqueue"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_queue(ACD_QUEUE_NAME,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
