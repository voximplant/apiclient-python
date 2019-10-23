from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the skill 1.

    SKILL_ID = 1
    
    try:
        res = voxapi.del_skill(skill_id=SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
