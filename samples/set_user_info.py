from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Edit the user password.

    USER_ID = 1
    USER_PASSWORD = "7654321"
    
    try:
        res = voxapi.set_user_info(user_id=USER_ID,
            user_password=USER_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
