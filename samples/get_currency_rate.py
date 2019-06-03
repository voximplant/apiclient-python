from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the current currency rates: RUR/USD and EUR/USD.

    CURRENCY = ["RUR", "EUR"]
    
    res = voxapi.get_currency_rate(CURRENCY)
    print(res)
