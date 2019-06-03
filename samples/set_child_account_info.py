from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Disable the child account.

    CHILD_ACCOUNT_ID = 1321
    ACTIVE = False
    
    res = voxapi.set_child_account_info(child_account_id=CHILD_ACCOUNT_ID, active=ACTIVE)
    print(res)
