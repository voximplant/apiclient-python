from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Change the skill name.

    NEW_SKILL_NAME = "Support"
    SKILL_ID = 1
    
    try:
        res = voxapi.set_skill_info(NEW_SKILL_NAME,
            skill_id=SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
