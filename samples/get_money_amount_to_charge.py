from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the recommended money amount to charge in USD.

    CURRENCY = "USD"
    
    try:
        res = voxapi.get_money_amount_to_charge(currency=CURRENCY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
