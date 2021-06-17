from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Edit the queue with id = 1.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = 1
    NEW_SQ_QUEUE_NAME = "myNewSmartQueue"
    
    try:
        res = voxapi.sq__set_queue_info(APPLICATION_ID,
            SQ_QUEUE_ID,
            new_sq_queue_name=NEW_SQ_QUEUE_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
