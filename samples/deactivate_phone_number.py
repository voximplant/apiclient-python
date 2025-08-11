from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Deactivate the phone 1.

    PHONE_ID = 1
    
    try:
        res = voxapi.deactivate_phone_number(phone_id=PHONE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
