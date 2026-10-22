from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Change the IM plan.

    PLAN_SUBSCRIPTION_TEMPLATE_ID = 3
    PLAN_TYPE = "IM"
    
    try:
        res = voxapi.change_account_plan(PLAN_SUBSCRIPTION_TEMPLATE_ID,
            plan_type=PLAN_TYPE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
