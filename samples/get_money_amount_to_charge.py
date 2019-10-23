from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the recommended money amount to charge in USD.

    CURRENCY = "USD"
    
    try:
        res = voxapi.get_money_amount_to_charge(currency=CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
