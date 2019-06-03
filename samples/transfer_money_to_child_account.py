from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Transfer the all money from the child account 1 to the parent account.

    CHILD_ACCOUNT_ID = 1
    AMOUNT = "-10000000"
    STRICT_MODE = False
    
    res = voxapi.transfer_money_to_child_account(CHILD_ACCOUNT_ID, AMOUNT, strict_mode=STRICT_MODE)
    print(res)
