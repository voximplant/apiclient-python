from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all rules from the all applications.

    RULE_ID = "all"
    APPLICATION_ID = "all"
    
    try:
        res = voxapi.del_rule(rule_id=RULE_ID, application_id=APPLICATION_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
