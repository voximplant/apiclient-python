from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Try remove link with record_id is 1.

    RECORD_ID = 1
    
    try:
        res = voxapi.delete_record(record_id=RECORD_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
