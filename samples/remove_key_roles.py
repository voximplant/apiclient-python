from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Remove the roles 1, 2, 3 from the key.

    KEY_ID = "ab81c90e-543e-4446-9af9-105269dfafca"
    ROLE_ID = [1, 2, 3]
    
    try:
        res = voxapi.remove_key_roles(KEY_ID,
            role_id=ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
