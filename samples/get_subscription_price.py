from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the all subscription template prices.

    
    try:
        res = voxapi.get_subscription_price()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
