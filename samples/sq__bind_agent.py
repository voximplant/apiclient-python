from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind the agent with id 1 and 2 to the queue with id = 1.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = 1
    USER_ID = 1
    
    try:
        res = voxapi.sq__bind_agent(APPLICATION_ID,
            SQ_QUEUE_ID,
            USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
