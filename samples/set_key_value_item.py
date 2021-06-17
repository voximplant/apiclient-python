from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # SetKeyValueItem example.

    KEY = "key1"
    VALUE = "value1"
    APPLICATION_ID = 1
    TTL = 864000
    
    try:
        res = voxapi.set_key_value_item(KEY,
            VALUE,
            APPLICATION_ID,
            ttl=TTL)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
