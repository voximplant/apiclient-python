from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Edit the queue with id = 1.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = 1
    NEW_SQ_QUEUE_NAME = "myNewSmartQueue"
    
    try:
        res = voxapi.sq__set_queue_info(application_id=APPLICATION_ID,
            sq_queue_id=SQ_QUEUE_ID,
            new_sq_queue_name=NEW_SQ_QUEUE_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
