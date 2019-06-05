from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the ACD queue 1.

    ACD_QUEUE_ID = 1
    
    try:
        res = voxapi.del_queue(acd_queue_id=ACD_QUEUE_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
