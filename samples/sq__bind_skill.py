from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Bind the skills with id 1 and 2 to all users.

    SQ_SKILLS = "[{\"sq_skill_id\":1,\"sq_skill_level\":1},{\"sq_skill_id\":2,\"sq_skill_level\":5}]"
    APPLICATION_ID = 1
    USER_ID = "all"
    
    try:
        res = voxapi.sq__bind_skill(SQ_SKILLS,
            application_id=APPLICATION_ID,
            user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
