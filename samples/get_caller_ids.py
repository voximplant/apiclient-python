from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the two callerIDs.

    COUNT = 2
    
    try:
        res = voxapi.get_caller_ids(count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
