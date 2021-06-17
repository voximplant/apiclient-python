from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind the skills with id 1 and 2 to all users.

    APPLICATION_ID = 1
    USER_ID = "all"
    SQ_SKILLS = "[{\"sq_skill_id\":1,\"sq_skill_level\":1},{\"sq_skill_id\":2,\"sq_skill_level\":5}]"
    
    try:
        res = voxapi.sq__bind_skill(APPLICATION_ID,
            USER_ID,
            SQ_SKILLS)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
