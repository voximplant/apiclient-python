from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    CALLERID_NUMBER = "74953331122"
    
    try:
        res = voxapi.add_caller_id(CALLERID_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
