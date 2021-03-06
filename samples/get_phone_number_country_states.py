from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the USA states.

    COUNTRY_CODE = "US"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    
    try:
        res = voxapi.get_phone_number_country_states(COUNTRY_CODE,
            PHONE_CATEGORY_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
