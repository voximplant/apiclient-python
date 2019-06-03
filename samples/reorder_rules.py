from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Set the rule selection order: 1, 7, 3

    RULE_ID = [1, 7, 3]
    
    res = voxapi.reorder_rules(RULE_ID)
    print(res)
