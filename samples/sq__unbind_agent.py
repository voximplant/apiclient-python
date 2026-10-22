from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Unbind the agent with id 1 from all queues.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = "all"
    USER_ID = 1
    
    try:
        res = voxapi.sq__unbind_agent(application_id=APPLICATION_ID,
            sq_queue_id=SQ_QUEUE_ID,
            user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
