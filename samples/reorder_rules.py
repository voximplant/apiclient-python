from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Set the rule selection order: 1, 7, 3.

    RULE_ID = [1, 7, 3]
    
    try:
        res = voxapi.reorder_rules(RULE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
