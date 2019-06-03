from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the Russian regions of the phone numbers.

    COUNTRY_CODE = "RU"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    
    res = voxapi.get_phone_number_regions(COUNTRY_CODE, PHONE_CATEGORY_NAME)
    print(res)
