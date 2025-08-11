from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Attach a US phone number to the account 1.

    COUNTRY_CODE = "US"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_ID = 1100
    COUNTRY_STATE = "CA"
    PHONE_COUNT = 1
    
    try:
        res = voxapi.attach_phone_number(COUNTRY_CODE,
            PHONE_CATEGORY_NAME,
            PHONE_REGION_ID,
            country_state=COUNTRY_STATE,
            phone_count=PHONE_COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
