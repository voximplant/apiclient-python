from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all scenarios.

    SCENARIO_ID = "all"
    
    res = voxapi.del_scenario(scenario_id=SCENARIO_ID)
    print(res)
