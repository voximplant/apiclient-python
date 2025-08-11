from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the all phone number categories.

    
    try:
        res = voxapi.get_phone_number_categories()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
