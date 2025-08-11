from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    PSTN_BLACKLIST_ID = 1
    
    try:
        res = voxapi.del_pstn_black_list_item(PSTN_BLACKLIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
