from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get regions with city AACHEN.

    COUNTRY_CODE = "DE"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    CITY_NAME = "AACHEN"
    
    try:
        res = voxapi.get_regions(COUNTRY_CODE,
            PHONE_CATEGORY_NAME,
            city_name=CITY_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
