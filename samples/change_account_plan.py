from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Change the IM plan.

    PLAN_TYPE = "IM"
    PLAN_SUBSCRIPTION_TEMPLATE_ID = 3
    
    try:
        res = voxapi.change_account_plan(PLAN_TYPE,
            plan_subscription_template_id=PLAN_SUBSCRIPTION_TEMPLATE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
