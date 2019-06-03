from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all rules from the all applications.

    RULE_ID = "all"
    APPLICATION_ID = "all"
    
    res = voxapi.del_rule(rule_id=RULE_ID, application_id=APPLICATION_ID)
    print(res)
