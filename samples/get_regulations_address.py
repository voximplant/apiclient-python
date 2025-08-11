from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Search regulation address with ID = 1.

    REGULATION_ADDRESS_ID = 1
    
    try:
        res = voxapi.get_regulations_address(regulation_address_id=REGULATION_ADDRESS_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
