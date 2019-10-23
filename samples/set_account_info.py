from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Change the account's password.

    NEW_ACCOUNT_PASSWORD = "7654321"
    
    try:
        res = voxapi.set_account_info(new_account_password=NEW_ACCOUNT_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
