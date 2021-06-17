from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Unbind the skill with id = 1 from the user with id = 1.

    APPLICATION_ID = 1
    USER_ID = 1
    SQ_SKILL_ID = 1
    
    try:
        res = voxapi.sq__unbind_skill(APPLICATION_ID,
            USER_ID,
            SQ_SKILL_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
