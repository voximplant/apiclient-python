from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    CALLERID_NUMBER = "74953331122"
    
    res = voxapi.add_caller_id(CALLERID_NUMBER)
    print(res)
