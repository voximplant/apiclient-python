from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the first rule for the template 74951234567.

    APPLICATION_ID = 1
    TEMPLATE = "74951234567"
    WITH_SCENARIOS = True
    COUNT = 1
    
    try:
        res = voxapi.get_rules(application_id=APPLICATION_ID,
            template=TEMPLATE,
            with_scenarios=WITH_SCENARIOS,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
