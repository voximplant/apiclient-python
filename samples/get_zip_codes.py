from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Search zip codes in Germany

    COUNTRY_CODE = "DE"
    COUNT = 1
    
    res = voxapi.get_zip_codes(COUNTRY_CODE, count=COUNT)
    print(res)
