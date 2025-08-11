from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete the rule 1 and 3.

    RULE_ID = [1, 3]
    
    try:
        res = voxapi.del_rule(rule_id=RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
