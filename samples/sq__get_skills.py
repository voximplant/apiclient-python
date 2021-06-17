from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the skills with id 2 and 4

    APPLICATION_ID = 1
    SQ_SKILL_ID = 2
    
    try:
        res = voxapi.sq__get_skills(APPLICATION_ID,
            sq_skill_id=SQ_SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
