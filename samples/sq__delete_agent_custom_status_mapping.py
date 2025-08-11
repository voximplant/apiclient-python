from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Remove a mapping for sq_status_name = READY.

    APPLICATION_ID = 1
    SQ_STATUS_NAME = "READY"
    
    try:
        res = voxapi.sq__delete_agent_custom_status_mapping(APPLICATION_ID,
            sq_status_name=SQ_STATUS_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
