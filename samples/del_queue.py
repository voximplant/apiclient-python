from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the ACD queue 1.

    ACD_QUEUE_ID = 1
    
    res = voxapi.del_queue(acd_queue_id=ACD_QUEUE_ID)
    print(res)
