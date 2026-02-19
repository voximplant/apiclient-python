from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the specified children.

    CHILD_ACCOUNT_ID = [414877, 464478]
    
    try:
        res = voxapi.get_children_accounts(child_account_id=CHILD_ACCOUNT_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
