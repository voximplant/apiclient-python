from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new scenario: var s='hello';

    SCENARIO_NAME = "scen1"
    SCENARIO_SCRIPT = "var s=\"hello\";"
    
    res = voxapi.add_scenario(SCENARIO_NAME, SCENARIO_SCRIPT)
    print(res)
