from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all users bound to the 'myapp1' application.

    USER_ID = "all"
    APPLICATION_NAME = "myapp1"
    
    try:
        res = voxapi.del_user(user_id=USER_ID, application_name=APPLICATION_NAME)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
