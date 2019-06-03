from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the skill 1.

    SKILL_ID = 1
    
    res = voxapi.del_skill(skill_id=SKILL_ID)
    print(res)
