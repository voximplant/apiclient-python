from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the current currency rate: RUR/USD.

    CURRENCY = "RUR"
    
    try:
        res = voxapi.get_currency_rate(CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
