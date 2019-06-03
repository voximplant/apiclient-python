from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the price to call to the phone number 79263332211

    RESOURCE_TYPE = "PSTNOUT"
    RESOURCE_PARAM = "79263332211"
    
    res = voxapi.get_resource_price(resource_type=RESOURCE_TYPE, resource_param=RESOURCE_PARAM)
    print(res)
