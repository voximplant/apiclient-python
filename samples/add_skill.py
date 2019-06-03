from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new skill.

    SKILL_NAME = "English"
    
    res = voxapi.add_skill(SKILL_NAME)
    print(res)
