from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Set the scenario loading order: 17, 15, 20.

    RULE_ID = 2
    SCENARIO_ID = [17, 15, 20]
    
    try:
        res = voxapi.reorder_scenarios(rule_id=RULE_ID,
            scenario_id=SCENARIO_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
