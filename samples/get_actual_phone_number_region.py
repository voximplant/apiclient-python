from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the Germany region of the phone numbers.

    COUNTRY_CODE = "DE"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    PHONE_REGION_ID = 1
    
    try:
        res = voxapi.get_actual_phone_number_region(COUNTRY_CODE,
            PHONE_CATEGORY_NAME,
            PHONE_REGION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
