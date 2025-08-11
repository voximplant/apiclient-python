from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the Russian regions of the phone numbers.

    COUNTRY_CODE = "RU"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    
    try:
        res = voxapi.get_phone_number_regions(COUNTRY_CODE,
            PHONE_CATEGORY_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
