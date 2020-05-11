from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the eligible subscription templates.

    
    try:
        res = voxapi.get_child_account_subscription_templates()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
