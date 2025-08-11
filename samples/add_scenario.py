from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new scenario: var s='hello';

    SCENARIO_NAME = "call_scenario"
    SCENARIO_SCRIPT = "var s=\"hello\";"
    
    try:
        res = voxapi.add_scenario(SCENARIO_NAME,
            scenario_script=SCENARIO_SCRIPT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
