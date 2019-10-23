from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    PSTN_BLACKLIST_ID = 1
    PSTN_BLACKLIST_PHONE = "123456789"
    
    try:
        res = voxapi.set_pstn_black_list_item(PSTN_BLACKLIST_ID,
            PSTN_BLACKLIST_PHONE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
