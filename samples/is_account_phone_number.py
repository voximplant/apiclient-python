from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Check if the phone number belongs to the account.

    PHONE_NUMBER = "79991234567"
    
    try:
        res = voxapi.is_account_phone_number(PHONE_NUMBER)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
