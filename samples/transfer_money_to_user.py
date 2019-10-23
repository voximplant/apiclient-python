from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Transfer 5.67 $ to the user 1 and transfer 5.67 $ to the user 2 too.
    # The account spends 2*5.67= 11.34 $ in total.

    AMOUNT = "5.67"
    USER_ID = [1, 2]
    CURRENCY = "USD"
    
    try:
        res = voxapi.transfer_money_to_user(AMOUNT,
            user_id=USER_ID,
            currency=CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
