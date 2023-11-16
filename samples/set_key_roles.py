from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Set roles 1, 2, 3 for the key.

    KEY_ID = "ab81c76e-573e-4046-9af9-105269dfafca"
    ROLE_ID = [1, 2, 3]
    
    try:
        res = voxapi.set_key_roles(KEY_ID,
            role_id=ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
