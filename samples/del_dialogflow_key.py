from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Remove key.

    DIALOGFLOW_KEY_ID = 1
    
    try:
        res = voxapi.del_dialogflow_key(DIALOGFLOW_KEY_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
