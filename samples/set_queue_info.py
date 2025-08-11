from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Change the queue name.

    ACD_QUEUE_ID = 1
    NEW_ACD_QUEUE_NAME = "support"
    
    try:
        res = voxapi.set_queue_info(acd_queue_id=ACD_QUEUE_ID,
            new_acd_queue_name=NEW_ACD_QUEUE_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
