from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    SIP_WHITELIST_ID = 1
    SIP_WHITELIST_NETWORK = "192.168.1.5/16"
    
    try:
        res = voxapi.set_sip_white_list_item(SIP_WHITELIST_ID,
            SIP_WHITELIST_NETWORK)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
