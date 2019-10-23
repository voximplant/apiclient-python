from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add a new rule.

    RULE_NAME = "allowall"
    RULE_PATTERN = ".*"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_rule(RULE_NAME,
            RULE_PATTERN,
            application_id=APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
