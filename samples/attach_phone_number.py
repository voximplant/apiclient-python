from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Attach the '74953332211' phone number to the account 1.

    COUNTRY_CODE = "RU"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_ID = 4
    PHONE_NUMBER = "74953332211"
    
    res = voxapi.attach_phone_number(COUNTRY_CODE, PHONE_CATEGORY_NAME, PHONE_REGION_ID, phone_number=PHONE_NUMBER)
    print(res)
