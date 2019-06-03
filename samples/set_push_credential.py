from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Modify credentials.

    PUSH_CREDENTIAL_ID = 1
    EXTERNAL_APP_NAME = "testapp"
    CERT_PASSWORD = "1234567"
    
    res = voxapi.set_push_credential(PUSH_CREDENTIAL_ID, EXTERNAL_APP_NAME, cert_password=CERT_PASSWORD)
    print(res)
