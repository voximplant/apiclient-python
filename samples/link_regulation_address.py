from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Link the regulation address to a phone number.

    REGULATION_ADDRESS_ID = 1
    PHONE_ID = 1
    
    try:
        res = voxapi.link_regulation_address(REGULATION_ADDRESS_ID,
            phone_id=PHONE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
