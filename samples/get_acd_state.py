from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the state of the queue 1.

    ACD_QUEUE_ID = 1
    
    res = voxapi.get_acd_state(acd_queue_id=ACD_QUEUE_ID)
    print(res)
