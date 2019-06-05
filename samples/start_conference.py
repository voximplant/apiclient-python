from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Start the conference from the user 1.

    CONFERENCE_NAME = "boss"
    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    USER_ID = 1
    
    try:
        res = voxapi.start_conference(CONFERENCE_NAME, RULE_ID, script_custom_data=SCRIPT_CUSTOM_DATA, user_id=USER_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
