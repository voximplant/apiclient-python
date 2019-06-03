from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the all applications.

    APPLICATION_ID = "all"
    
    res = voxapi.del_application(application_id=APPLICATION_ID)
    print(res)
