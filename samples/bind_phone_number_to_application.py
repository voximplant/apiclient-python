from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Bind the phone 1 to the application 1.

    PHONE_ID = 1
    APPLICATION_ID = 1
    
    try:
        res = voxapi.bind_phone_number_to_application(phone_id=PHONE_ID,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
