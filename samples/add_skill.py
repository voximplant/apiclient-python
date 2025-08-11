from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new skill.

    SKILL_NAME = "English"
    
    try:
        res = voxapi.add_skill(SKILL_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
