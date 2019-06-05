from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get Germany

    COUNTRY_CODE = "DE"
    
    try:
        res = voxapi.get_countries(country_code=COUNTRY_CODE)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
