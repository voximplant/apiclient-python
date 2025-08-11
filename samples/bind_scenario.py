from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Bind the scenarios 1, 2 and 3 with the rule 1.

    SCENARIO_ID = [1, 2, 3]
    RULE_ID = 1
    
    try:
        res = voxapi.bind_scenario(scenario_id=SCENARIO_ID,
            rule_id=RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
