from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Transfer 5.67 $ to the child account 1 and transfer 5.67 $ to the
    # child account 2 too. The parent account spends 2*5.67= 11.34 $ in
    # total.

    CHILD_ACCOUNT_ID = [1, 2]
    AMOUNT = "5.67"
    CURRENCY = "USD"
    
    try:
        res = voxapi.transfer_money_to_child_account(CHILD_ACCOUNT_ID,
            AMOUNT,
            currency=CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
