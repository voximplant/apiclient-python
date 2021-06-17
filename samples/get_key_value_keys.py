from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # GetKeyValueKeys example.

    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_key_value_keys(APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
