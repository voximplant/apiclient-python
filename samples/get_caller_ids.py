from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Try to find the 79997770044 CID.

    CALLERID_NUMBER = "79997770044"
    
    res = voxapi.get_caller_ids(callerid_number=CALLERID_NUMBER)
    print(res)
