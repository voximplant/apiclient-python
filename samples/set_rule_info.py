from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Deny all.

    RULE_ID = 1
    RULE_NAME = "denyall"
    RULE_PATTERN_EXCLUDE = ".*"
    
    res = voxapi.set_rule_info(RULE_ID, rule_name=RULE_NAME, rule_pattern_exclude=RULE_PATTERN_EXCLUDE)
    print(res)
