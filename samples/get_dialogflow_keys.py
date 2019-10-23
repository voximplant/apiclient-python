from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get push credentials.

    DIALOGFLOW_KEY_ID = 1
    
    try:
        res = voxapi.get_dialogflow_keys(dialogflow_key_id=DIALOGFLOW_KEY_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
