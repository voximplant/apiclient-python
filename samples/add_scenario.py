from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new scenario: var s='hello';

    SCENARIO_NAME = "scen1"
    SCENARIO_SCRIPT = "var s=\"hello\";"
    
    try:
        res = voxapi.add_scenario(SCENARIO_NAME, SCENARIO_SCRIPT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
