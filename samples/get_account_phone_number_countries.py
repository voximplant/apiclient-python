from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the countries where the account with id = 1 has phone numbers
    # attached to the application with id = 1.

    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_account_phone_number_countries(application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
