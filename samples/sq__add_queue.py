from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new queue.

    SQ_QUEUE_NAME = "smartQueue1"
    CALL_AGENT_SELECTION = "MOST_QUALIFIED"
    CALL_TASK_SELECTION = "MAX_WAITING_TIME"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.sq__add_queue(SQ_QUEUE_NAME,
            CALL_AGENT_SELECTION,
            CALL_TASK_SELECTION,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
