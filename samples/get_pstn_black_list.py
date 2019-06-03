from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    
    res = voxapi.get_pstn_black_list()
    print(res)
