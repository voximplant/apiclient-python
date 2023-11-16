from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the status mappings.

    APPLICATION_ID = 1
    
    try:
        res = voxapi.sq__get_agent_custom_status_mapping(application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
