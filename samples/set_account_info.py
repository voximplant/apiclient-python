from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Change the account's password.

    NEW_ACCOUNT_PASSWORD = "7654321"
    
    try:
        res = voxapi.set_account_info(new_account_password=NEW_ACCOUNT_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
