from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the rule 1 and 3.

    RULE_ID = [1, 3]
    
    try:
        res = voxapi.del_rule(rule_id=RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
