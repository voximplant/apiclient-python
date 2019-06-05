from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the SIP registration subscription template.

    SUBSCRIPTION_TEMPLATE_TYPE = "SIP_REGISTRATION"
    
    try:
        res = voxapi.get_subscription_price(subscription_template_type=SUBSCRIPTION_TEMPLATE_TYPE)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
