from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    SIP_WHITELIST_ID = 1
    
    res = voxapi.del_sip_white_list_item(SIP_WHITELIST_ID)
    print(res)
