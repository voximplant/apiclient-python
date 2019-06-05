from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    CALLERID_NUMBER = "74953331122"
    
    try:
        res = voxapi.add_caller_id(CALLERID_NUMBER)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
