from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Edit a skill.

    APPLICATION_ID = 1
    SQ_SKILL_ID = 1
    NEW_SQ_SKILL_NAME = "newSkill"
    
    try:
        res = voxapi.sq__set_skill_info(application_id=APPLICATION_ID,
            sq_skill_id=SQ_SKILL_ID,
            new_sq_skill_name=NEW_SQ_SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
