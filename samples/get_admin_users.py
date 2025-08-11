from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get two first admin users.

    WITH_ACCESS_ENTRIES = True
    COUNT = 2
    
    try:
        res = voxapi.get_admin_users(with_access_entries=WITH_ACCESS_ENTRIES,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
