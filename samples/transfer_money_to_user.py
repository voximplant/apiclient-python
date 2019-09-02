from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Transfer the all money from the user 1 to the parent account.

    AMOUNT = "-10000000"
    USER_ID = 1
    STRICT_MODE = False
    
    try:
        res = voxapi.transfer_money_to_user(AMOUNT, user_id=USER_ID, strict_mode=STRICT_MODE)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
