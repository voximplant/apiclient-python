from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Change the queue name.

    ACD_QUEUE_ID = 1
    NEW_ACD_QUEUE_NAME = "support"
    
    res = voxapi.set_queue_info(acd_queue_id=ACD_QUEUE_ID, new_acd_queue_name=NEW_ACD_QUEUE_NAME)
    print(res)
