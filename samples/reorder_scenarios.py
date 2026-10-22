from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Set the scenario loading order: 17, 15, 20.

    SCENARIO_ID = [17, 15, 20]
    RULE_ID = 2
    
    try:
        res = voxapi.reorder_scenarios(SCENARIO_ID,
            rule_id=RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
