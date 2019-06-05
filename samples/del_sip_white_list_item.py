from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    SIP_WHITELIST_ID = 1
    
    try:
        res = voxapi.del_sip_white_list_item(SIP_WHITELIST_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
