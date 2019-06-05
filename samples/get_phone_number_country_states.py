from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the AL (Alabama) state info.

    COUNTRY_CODE = "US"
    PHONE_CATEGORY_NAME = "GEOGRAPHIC"
    COUNTRY_STATE = "AL"
    
    try:
        res = voxapi.get_phone_number_country_states(COUNTRY_CODE, PHONE_CATEGORY_NAME, country_state=COUNTRY_STATE)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
