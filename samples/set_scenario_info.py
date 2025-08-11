from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new scenario: var s='hello';

    SCENARIO_ID = 1
    SCENARIO_NAME = "call_scenario"
    SCENARIO_SCRIPT = "var s=\"hello world\";"
    
    try:
        res = voxapi.set_scenario_info(scenario_id=SCENARIO_ID,
            scenario_name=SCENARIO_NAME,
            scenario_script=SCENARIO_SCRIPT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
