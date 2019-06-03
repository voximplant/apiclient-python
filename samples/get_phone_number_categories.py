from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the phone number categories in Russia.

    COUNTRY_CODE = "RU"
    
    res = voxapi.get_phone_number_categories(country_code=COUNTRY_CODE)
    print(res)
