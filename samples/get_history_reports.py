from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all the reports.

    HISTORY_TYPE = "all"
    
    try:
        res = voxapi.get_history_reports(history_type=HISTORY_TYPE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
