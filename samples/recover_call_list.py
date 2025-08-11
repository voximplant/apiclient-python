from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Restore list with id = 1.

    LIST_ID = 1
    
    try:
        res = voxapi.recover_call_list(LIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
