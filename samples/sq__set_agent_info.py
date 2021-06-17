from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
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
    
