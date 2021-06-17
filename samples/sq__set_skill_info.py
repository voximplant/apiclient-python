from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Edit a skill.

    APPLICATION_ID = 1
    SQ_SKILL_ID = 1
    NEW_SQ_SKILL_NAME = "newSkill"
    
    try:
        res = voxapi.sq__set_skill_info(APPLICATION_ID,
            SQ_SKILL_ID,
            new_sq_skill_name=NEW_SQ_SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
