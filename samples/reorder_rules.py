from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Set the rule selection order: 1, 7, 3

    RULE_ID = [1, 7, 3]
    
    try:
        res = voxapi.reorder_rules(RULE_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
