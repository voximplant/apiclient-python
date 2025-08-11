from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Change the skill name.

    NEW_SKILL_NAME = "Support"
    SKILL_ID = 1
    
    try:
        res = voxapi.set_skill_info(NEW_SKILL_NAME,
            skill_id=SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
