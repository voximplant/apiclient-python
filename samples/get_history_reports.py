from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all the reports.

    HISTORY_TYPE = "all"
    
    res = voxapi.get_history_reports(history_type=HISTORY_TYPE)
    print(res)
