from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    PSTN_BLACKLIST_PHONE = "123456789"
    
    try:
        res = voxapi.add_pstn_black_list_item(PSTN_BLACKLIST_PHONE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
