from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Bind the agent with id 1 and 2 to the queue with id = 1.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = "1"
    USER_ID = [1, 2]
    
    try:
        res = voxapi.sq__bind_agent(APPLICATION_ID,
            SQ_QUEUE_ID,
            USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
