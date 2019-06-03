from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the recommended money amount to charge in USD.

    CURRENCY = "USD"
    
    res = voxapi.get_money_amount_to_charge(currency=CURRENCY)
    print(res)
