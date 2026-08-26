from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Bind three users to one queue.

    APPLICATION_ID = 1
    USER_ID = [12, 987, 456]
    ACD_QUEUE_NAME = "myqueue"
    BIND = True
    
    try:
        res = voxapi.bind_user_to_queue(application_id=APPLICATION_ID,
            user_id=USER_ID,
            acd_queue_name=ACD_QUEUE_NAME,
            bind=BIND)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
