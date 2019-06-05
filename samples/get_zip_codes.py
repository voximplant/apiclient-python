from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Search zip codes in Germany

    COUNTRY_CODE = "DE"
    COUNT = 1
    
    try:
        res = voxapi.get_zip_codes(COUNTRY_CODE, count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
