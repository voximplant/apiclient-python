from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the SIP registration subscription template.

    SUBSCRIPTION_TEMPLATE_TYPE = "SIP_REGISTRATION"
    
    res = voxapi.get_subscription_price(subscription_template_type=SUBSCRIPTION_TEMPLATE_TYPE)
    print(res)
