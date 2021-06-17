from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Unbind the agent with id 1 from all queues.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = "all"
    USER_ID = 1
    
    try:
        res = voxapi.sq__unbind_agent(APPLICATION_ID,
            SQ_QUEUE_ID,
            USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
