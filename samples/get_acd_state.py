from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the state of the queue 1.

    ACD_QUEUE_ID = 1
    
    try:
        res = voxapi.get_acd_state(acd_queue_id=ACD_QUEUE_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
