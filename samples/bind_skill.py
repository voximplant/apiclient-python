from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Unbind the skills 1, 6 from the all users and the queues 11, 12.

    SKILL_ID = [1, 6]
    ACD_QUEUE_ID = [11, 12]
    USER_ID = "all"
    
    try:
        res = voxapi.bind_skill(skill_id=SKILL_ID, acd_queue_id=ACD_QUEUE_ID, user_id=USER_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
