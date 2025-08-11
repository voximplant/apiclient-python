from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add a new admin role with the GetAccountInfo and GetCallHistory
    # permissions.

    ADMIN_ROLE_NAME = "read_only"
    ALLOWED_ENTRIES = ["GetAccountInfo", "GetCallHistory"]
    
    try:
        res = voxapi.add_admin_role(ADMIN_ROLE_NAME,
            allowed_entries=ALLOWED_ENTRIES)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
