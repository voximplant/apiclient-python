from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    SIP_WHITELIST_ID = 1
    
    try:
        res = voxapi.del_sip_white_list_item(SIP_WHITELIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
