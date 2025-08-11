from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get all the queues.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = [1, 2]
    
    try:
        res = voxapi.sq__get_queues(APPLICATION_ID,
            sq_queue_id=SQ_QUEUE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
