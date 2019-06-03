from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the particular child.

    CHILD_ACCOUNT_EMAIL = "mychild@gmail.com"
    
    res = voxapi.get_children_accounts(child_account_email=CHILD_ACCOUNT_EMAIL)
    print(res)
