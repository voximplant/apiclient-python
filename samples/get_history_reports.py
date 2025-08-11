from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get all the reports.

    HISTORY_TYPE = "all"
    
    try:
        res = voxapi.get_history_reports(history_type=HISTORY_TYPE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
