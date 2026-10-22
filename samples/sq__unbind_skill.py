from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Unbind the skill with id = 1 from the user with id = 1.

    APPLICATION_ID = 1
    USER_ID = 1
    SQ_SKILL_ID = 1
    
    try:
        res = voxapi.sq__unbind_skill(application_id=APPLICATION_ID,
            user_id=USER_ID,
            sq_skill_id=SQ_SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
