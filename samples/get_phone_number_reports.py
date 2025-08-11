from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get all the reports.

    
    try:
        res = voxapi.get_phone_number_reports()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
