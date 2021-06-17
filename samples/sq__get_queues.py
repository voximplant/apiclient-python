from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all the queues.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = 1
    
    try:
        res = voxapi.sq__get_queues(APPLICATION_ID,
            sq_queue_id=SQ_QUEUE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
