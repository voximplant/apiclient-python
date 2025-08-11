from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    KEY_ID = "ab81c66e-570e-4446-9af9-105269dfafca"
    
    try:
        res = voxapi.delete_key(KEY_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
