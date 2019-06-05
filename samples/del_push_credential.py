from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Remove credentials.

    PUSH_CREDENTIAL_ID = 1
    
    try:
        res = voxapi.del_push_credential(PUSH_CREDENTIAL_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
