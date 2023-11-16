from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the time agents spent in the ONLINE status for all SmartQueues
    # within one application.

    REPORT_TYPE = "sum_agents_online_time"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_smart_queue_day_history(REPORT_TYPE,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
