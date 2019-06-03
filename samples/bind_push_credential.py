from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind the push credential to the application.

    PUSH_CREDENTIAL_ID = 1
    APPLICATION_ID = 1
    
    res = voxapi.bind_push_credential(PUSH_CREDENTIAL_ID, APPLICATION_ID)
    print(res)
