from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Deactivates the subscription with ID = 20 and
    # subscription_finish_date = September 29th 2019.

    SUBSCRIPTION_ID = 20
    CHILD_ACCOUNT_ID = 10
    SUBSCRIPTION_FINISH_DATE = datetime.datetime(2019, 9, 29, 0, 0, 0, pytz.utc)
    
    try:
        res = voxapi.deactivate_child_account_subscription(SUBSCRIPTION_ID,
            CHILD_ACCOUNT_ID,
            subscription_finish_date=SUBSCRIPTION_FINISH_DATE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
