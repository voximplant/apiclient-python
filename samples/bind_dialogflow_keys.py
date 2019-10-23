from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Bind a Dialogflow key to the application.

    DIALOGFLOW_KEY_ID = 1
    APPLICATION_ID = 1
    
    try:
        res = voxapi.bind_dialogflow_keys(DIALOGFLOW_KEY_ID,
            APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
