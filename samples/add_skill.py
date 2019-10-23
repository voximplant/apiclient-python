from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add a new skill.

    SKILL_NAME = "English"
    
    try:
        res = voxapi.add_skill(SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
