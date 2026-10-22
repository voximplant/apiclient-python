from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new skill.

    SQ_SKILL_NAME = "mySkill"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.sq__add_skill(SQ_SKILL_NAME,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
