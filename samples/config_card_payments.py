from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Enable the auto charging.

    AUTO_CHARGE = True
    MIN_BALANCE = "5"
    CARD_OVERRUN_VALUE = "10"
    
    try:
        res = voxapi.config_card_payments(auto_charge=AUTO_CHARGE,
            min_balance=MIN_BALANCE,
            card_overrun_value=CARD_OVERRUN_VALUE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
