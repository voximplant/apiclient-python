from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Try remove link with record_id is 1.

    RECORD_ID = 1
    
    res = voxapi.delete_record(record_id=RECORD_ID)
    print(res)
