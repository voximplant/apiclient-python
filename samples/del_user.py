from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all users bound to the 'myapp1' application.

    USER_ID = "all"
    APPLICATION_NAME = "myapp1"
    
    res = voxapi.del_user(user_id=USER_ID, application_name=APPLICATION_NAME)
    print(res)
