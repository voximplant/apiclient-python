from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Remove key.

    DIALOGFLOW_KEY_ID = 1
    
    res = voxapi.del_dialogflow_key(DIALOGFLOW_KEY_ID)
    print(res)
