from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new user.

    USER_NAME = "iden1"
    USER_DISPLAY_NAME = "iden1"
    USER_PASSWORD = "1234567"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_user(USER_NAME, USER_DISPLAY_NAME, USER_PASSWORD, application_id=APPLICATION_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
