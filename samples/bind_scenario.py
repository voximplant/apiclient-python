from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind the scenarios 1, 2 and 3 with the rule 1.

    SCENARIO_ID = [1, 2, 3]
    RULE_ID = 1
    
    res = voxapi.bind_scenario(scenario_id=SCENARIO_ID, rule_id=RULE_ID)
    print(res)
