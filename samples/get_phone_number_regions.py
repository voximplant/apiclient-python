from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the Russian regions of the phone numbers.

    COUNTRY_CODE = "RU"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    
    try:
        res = voxapi.get_phone_number_regions(COUNTRY_CODE,
            PHONE_CATEGORY_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
