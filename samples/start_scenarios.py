from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Start the scripts from the account.

    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    
    try:
        res = voxapi.start_scenarios(RULE_ID,
            script_custom_data=SCRIPT_CUSTOM_DATA)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
