from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    PSTN_BLACKLIST_ID = 1
    
    res = voxapi.del_pstn_black_list_item(PSTN_BLACKLIST_ID)
    print(res)
