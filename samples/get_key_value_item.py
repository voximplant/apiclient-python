from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # GetKeyValueItem example.

    KEY = "key1"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.get_key_value_item(KEY,
            APPLICATION_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
