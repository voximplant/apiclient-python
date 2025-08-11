from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Disable the child account.

    CHILD_ACCOUNT_ID = 1321
    ACTIVE = False
    
    try:
        res = voxapi.set_child_account_info(child_account_id=CHILD_ACCOUNT_ID,
            active=ACTIVE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
