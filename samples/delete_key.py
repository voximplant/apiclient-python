from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    KEY_ID = "ab81c66e-570e-4446-9af9-105269dfafca"
    
    try:
        res = voxapi.delete_key(KEY_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
