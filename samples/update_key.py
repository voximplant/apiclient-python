from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Create a new subuser for account_id = 1.

    KEY_ID = "ab98c70e-573e-4446-9af9-105269dfafca"
    DESCRIPTION = "test_desc"
    
    try:
        res = voxapi.update_key(KEY_ID, DESCRIPTION)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
