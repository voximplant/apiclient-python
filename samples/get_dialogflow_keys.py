from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get push credentials.

    DIALOGFLOW_KEY_ID = 1
    
    res = voxapi.get_dialogflow_keys(dialogflow_key_id=DIALOGFLOW_KEY_ID)
    print(res)
