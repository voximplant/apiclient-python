from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind three users to one queue.

    BIND = True
    APPLICATION_ID = 1
    USER_ID = [12, 987, 456]
    ACD_QUEUE_NAME = "myqueue"
    
    try:
        res = voxapi.bind_user_to_queue(BIND,
            application_id=APPLICATION_ID,
            user_id=USER_ID,
            acd_queue_name=ACD_QUEUE_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
