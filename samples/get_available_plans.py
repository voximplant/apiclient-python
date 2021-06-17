from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get allowed IM plans to change.

    PLAN_TYPE = "IM"
    
    try:
        res = voxapi.get_available_plans(plan_type=PLAN_TYPE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
