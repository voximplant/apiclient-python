from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
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
    
