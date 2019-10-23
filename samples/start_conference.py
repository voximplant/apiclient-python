from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Start the conference from the account.

    CONFERENCE_NAME = "boss"
    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    
    try:
        res = voxapi.start_conference(CONFERENCE_NAME,
            RULE_ID,
            script_custom_data=SCRIPT_CUSTOM_DATA)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
