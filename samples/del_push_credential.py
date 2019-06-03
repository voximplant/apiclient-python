from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Remove credentials.

    PUSH_CREDENTIAL_ID = 1
    
    res = voxapi.del_push_credential(PUSH_CREDENTIAL_ID)
    print(res)
