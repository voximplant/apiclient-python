from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    SIP_WHITELIST_ID = 1
    SIP_WHITELIST_NETWORK = "192.168.1.5/16"
    
    res = voxapi.set_sip_white_list_item(SIP_WHITELIST_ID, SIP_WHITELIST_NETWORK)
    print(res)
