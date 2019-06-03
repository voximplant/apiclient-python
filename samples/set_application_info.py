from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Change the application name.

    APPLICATION_ID = 1
    APPLICATION_NAME = "myapp11"
    
    res = voxapi.set_application_info(application_id=APPLICATION_ID, application_name=APPLICATION_NAME)
    print(res)
