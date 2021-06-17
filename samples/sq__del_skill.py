from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the skill with id = 5.

    APPLICATION_ID = 1
    SQ_SKILL_ID = 5
    
    try:
        res = voxapi.sq__del_skill(APPLICATION_ID,
            SQ_SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
