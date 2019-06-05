from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    PSTN_BLACKLIST_ID = 1
    
    try:
        res = voxapi.del_pstn_black_list_item(PSTN_BLACKLIST_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
