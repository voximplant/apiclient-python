from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the subscription with ID = 20.

    CHILD_ACCOUNT_ID = 10
    SUBSCRIPTION_ID = 20
    
    try:
        res = voxapi.get_child_account_subscriptions(CHILD_ACCOUNT_ID,
            subscription_id=SUBSCRIPTION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
