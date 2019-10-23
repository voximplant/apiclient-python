from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete two users with ID 3 and 55.

    USER_ID = [3, 55]
    
    try:
        res = voxapi.del_user(user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
