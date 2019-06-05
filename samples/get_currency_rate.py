from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the current currency rates: RUR/USD and EUR/USD.

    CURRENCY = ["RUR", "EUR"]
    
    try:
        res = voxapi.get_currency_rate(CURRENCY)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
