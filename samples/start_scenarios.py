from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Start the scripts from the user 1.

    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    USER_ID = 1
    
    res = voxapi.start_scenarios(RULE_ID, script_custom_data=SCRIPT_CUSTOM_DATA, user_id=USER_ID)
    print(res)
