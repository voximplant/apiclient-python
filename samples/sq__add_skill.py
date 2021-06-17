from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add a new skill.

    APPLICATION_ID = 1
    SQ_SKILL_NAME = "mySkill"
    
    try:
        res = voxapi.sq__add_skill(APPLICATION_ID,
            SQ_SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
