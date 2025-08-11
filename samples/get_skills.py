from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get two skills, but skip the first one.

    OFFSET = 1
    COUNT = 2
    
    try:
        res = voxapi.get_skills(offset=OFFSET,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
