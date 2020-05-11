from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Create a subscription for the child account with ID = 10 using the
    # subscription template with ID = 184.

    CHILD_ACCOUNT_ID = 10
    SUBSCRIPTION_TEMPLATE_ID = 184
    SUBSCRIPTION_NAME = "Meaningful subscription name"
    
    try:
        res = voxapi.add_child_account_subscription(CHILD_ACCOUNT_ID,
            SUBSCRIPTION_TEMPLATE_ID,
            subscription_name=SUBSCRIPTION_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
