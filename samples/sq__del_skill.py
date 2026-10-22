from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete the skill with id = 5.

    APPLICATION_ID = 1
    SQ_SKILL_ID = 5
    
    try:
        res = voxapi.sq__del_skill(application_id=APPLICATION_ID,
            sq_skill_id=SQ_SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
