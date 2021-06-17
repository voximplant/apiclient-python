from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the account's info.

    
    try:
        res = voxapi.get_account_info()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
