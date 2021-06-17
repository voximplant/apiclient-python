from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the queue with id = 3.

    APPLICATION_ID = 1
    SQ_QUEUE_ID = 3
    
    try:
        res = voxapi.sq__del_queue(APPLICATION_ID,
            SQ_QUEUE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
