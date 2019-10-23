from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind the skills 1, 5 to the users 5, 6, 10.

    SKILL_ID = [1, 3]
    USER_ID = [5, 6, 10]
    
    try:
        res = voxapi.bind_skill(skill_id=SKILL_ID,
            user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
