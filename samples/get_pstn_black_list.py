from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    try:
        res = voxapi.get_pstn_black_list()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
