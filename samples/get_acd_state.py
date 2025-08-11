from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the state of the queue 1.

    ACD_QUEUE_ID = 1
    
    try:
        res = voxapi.get_acd_state(acd_queue_id=ACD_QUEUE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
