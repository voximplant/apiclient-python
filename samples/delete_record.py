from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Try remove link with record_id is 1.

    RECORD_ID = 1
    
    try:
        res = voxapi.delete_record(record_id=RECORD_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
