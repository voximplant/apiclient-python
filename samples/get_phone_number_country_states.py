from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the USA states.

    COUNTRY_CODE = "US"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    
    try:
        res = voxapi.get_phone_number_country_states(COUNTRY_CODE,
            phone_category_name=PHONE_CATEGORY_NAME)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
