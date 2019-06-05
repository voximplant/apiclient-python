from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the particular child.

    CHILD_ACCOUNT_EMAIL = "mychild@gmail.com"
    
    try:
        res = voxapi.get_children_accounts(child_account_email=CHILD_ACCOUNT_EMAIL)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
