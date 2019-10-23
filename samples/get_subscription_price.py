from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the all subscription template prices.

    
    try:
        res = voxapi.get_subscription_price()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
