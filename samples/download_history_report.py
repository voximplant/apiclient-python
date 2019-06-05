from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Download the completed history report with id = 1

    HISTORY_REPORT_ID = 1
    
    try:
        res = voxapi.download_history_report(HISTORY_REPORT_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
