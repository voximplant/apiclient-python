from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new skill.

    APPLICATION_ID = 1
    SQ_SKILL_NAME = "mySkill"
    
    try:
        res = voxapi.sq__add_skill(APPLICATION_ID,
            SQ_SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
