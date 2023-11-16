from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add/rename a status depending on the presence of an internal status
    # in agent_status_mapping.

    SQ_STATUS_NAME = "READY"
    CUSTOM_STATUS_NAME = "ReadyForCall"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.sq__set_agent_custom_status_mapping(SQ_STATUS_NAME,
            CUSTOM_STATUS_NAME,
            APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
