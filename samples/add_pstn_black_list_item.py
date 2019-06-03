from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    PSTN_BLACKLIST_PHONE = "123456789"
    
    res = voxapi.add_pstn_black_list_item(PSTN_BLACKLIST_PHONE)
    print(res)
