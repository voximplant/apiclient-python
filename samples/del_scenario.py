from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all scenarios.

    SCENARIO_ID = "all"
    
    try:
        res = voxapi.del_scenario(scenario_id=SCENARIO_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
