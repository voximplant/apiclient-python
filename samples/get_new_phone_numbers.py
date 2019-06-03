from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the two new fixed Russian phone numbers at max.

    COUNTRY_CODE = "RU"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_ID = 1
    COUNT = 2
    
    res = voxapi.get_new_phone_numbers(COUNTRY_CODE, PHONE_CATEGORY_NAME, PHONE_REGION_ID, count=COUNT)
    print(res)
