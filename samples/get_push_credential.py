from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get push credentials.

    PUSH_CREDENTIAL_ID = 1
    
    res = voxapi.get_push_credential(push_credential_id=PUSH_CREDENTIAL_ID)
    print(res)
