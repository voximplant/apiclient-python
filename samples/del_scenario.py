from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the scenario 1 and 3.

    SCENARIO_ID = [1, 3]
    
    try:
        res = voxapi.del_scenario(scenario_id=SCENARIO_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
