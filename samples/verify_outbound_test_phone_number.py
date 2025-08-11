from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the verification code.

    
    try:
        res = voxapi.verify_outbound_test_phone_number()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
