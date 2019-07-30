from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get roles of the key.

    KEY_ID = "ab81c50e-573e-4446-9af9-105269dfafca"
    
    try:
        res = voxapi.get_key_roles(KEY_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
