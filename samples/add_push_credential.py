from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add new Google credentials.

    PUSH_PROVIDER_NAME = "GOOGLE"
    SENDER_ID = "704777431520"
    SERVER_KEY = "AAAAjM-LQsc:APA91bGyCb5WhcGtaM-RaOI1GqWps1Uh9K-YoY75HIBy-En-4piH4c6_50gIEbSaCfuDrsLNfyZCvteiu6EjxA_rEBOvlc4xZ30uiGgbuM_jdT6y6Ku55OwnCyIxRNznvmx1jkkLexSU"
    
    try:
        res = voxapi.add_push_credential(push_provider_name=PUSH_PROVIDER_NAME, sender_id=SENDER_ID, server_key=SERVER_KEY)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
