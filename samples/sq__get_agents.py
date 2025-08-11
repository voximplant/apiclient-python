from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get all agents with their current statuses.

    APPLICATION_ID = 1
    HANDLE_CALLS = False
    WITH_SQ_STATUSES = True
    
    try:
        res = voxapi.sq__get_agents(APPLICATION_ID,
            HANDLE_CALLS,
            with_sq_statuses=WITH_SQ_STATUSES)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
