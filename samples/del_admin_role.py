from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Delete the admin role.

    ADMIN_ROLE_ID = 10
    
    try:
        res = voxapi.del_admin_role(admin_role_id=ADMIN_ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
