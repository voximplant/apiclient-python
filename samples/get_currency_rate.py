from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the current currency rate: RUR/USD.

    CURRENCY = "RUR"
    
    try:
        res = voxapi.get_currency_rate(CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
