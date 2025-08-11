from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the phone number info.

    
    try:
        res = voxapi.get_outbound_test_phone_numbers()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
