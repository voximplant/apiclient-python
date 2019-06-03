from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Search regulation address with ID = 1

    REGULATION_ADDRESS_ID = 1
    
    res = voxapi.get_regulations_address(regulation_address_id=REGULATION_ADDRESS_ID)
    print(res)
