from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get Germany.

    COUNTRY_CODE = "DE"
    
    try:
        res = voxapi.get_countries(country_code=COUNTRY_CODE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
