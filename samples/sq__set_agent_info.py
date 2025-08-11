from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Edit settings of the agent with id = 2.

    APPLICATION_ID = 1
    USER_ID = 2
    HANDLE_CALLS = True
    
    try:
        res = voxapi.sq__set_agent_info(APPLICATION_ID,
            USER_ID,
            HANDLE_CALLS)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
