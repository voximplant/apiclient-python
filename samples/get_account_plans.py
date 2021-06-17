from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all account plans with packages.

    
    try:
        res = voxapi.get_account_plans()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
