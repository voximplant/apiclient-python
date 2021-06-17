from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the time agents spent in the DIALING status for all smart queues
    # within one application.

    REPORT_TYPE = "sum_agents_dialing_time"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_smart_queue_realtime_metrics(REPORT_TYPE,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
