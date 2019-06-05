from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the phone number categories in Russia.

    COUNTRY_CODE = "RU"
    
    try:
        res = voxapi.get_phone_number_categories(country_code=COUNTRY_CODE)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
