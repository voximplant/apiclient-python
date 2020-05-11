from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Modify credentials.

    PUSH_CREDENTIAL_ID = 1
    CERT_PASSWORD = "1234567"
    
    try:
        res = voxapi.set_push_credential(PUSH_CREDENTIAL_ID,
            cert_password=CERT_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
