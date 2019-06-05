from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get push credentials.

    PUSH_CREDENTIAL_ID = 1
    
    try:
        res = voxapi.get_push_credential(push_credential_id=PUSH_CREDENTIAL_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
