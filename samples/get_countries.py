from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get Germany

    COUNTRY_CODE = "DE"
    
    res = voxapi.get_countries(country_code=COUNTRY_CODE)
    print(res)
