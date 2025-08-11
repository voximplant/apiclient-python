from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a personal phone number.

    PHONE_NUMBER = "12223334444"
    
    try:
        res = voxapi.add_outbound_test_phone_number(PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
