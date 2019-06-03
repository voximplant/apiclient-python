from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Search available regulation address

    COUNTRY_CODE = "DE"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_CODE = "643"
    
    res = voxapi.get_available_regulations(COUNTRY_CODE, PHONE_CATEGORY_NAME, phone_region_code=PHONE_REGION_CODE)
    print(res)
