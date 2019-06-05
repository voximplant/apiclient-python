from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind the push credential to the application.

    PUSH_CREDENTIAL_ID = 1
    APPLICATION_ID = 1
    
    try:
        res = voxapi.bind_push_credential(PUSH_CREDENTIAL_ID, APPLICATION_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
