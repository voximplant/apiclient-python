from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the Germany region of the phone numbers.

    COUNTRY_CODE = "DE"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_ID = 1
    
    res = voxapi.get_actual_phone_number_region(COUNTRY_CODE, PHONE_CATEGORY_NAME, PHONE_REGION_ID)
    print(res)
