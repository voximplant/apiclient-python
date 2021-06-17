from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all agents with their current statuses.

    APPLICATION_ID = 1
    WITH_SQ_STATUSES = True
    
    try:
        res = voxapi.sq__get_agents(APPLICATION_ID,
            with_sq_statuses=WITH_SQ_STATUSES)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
