from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Add the 92.255.220.0/24 network to the white list.

    AUTHORIZED_IP = "92.255.220.0/24"
    
    try:
        res = voxapi.add_authorized_account_ip(AUTHORIZED_IP)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
