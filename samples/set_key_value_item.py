from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
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
    
