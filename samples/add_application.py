from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new application.

    APPLICATION_NAME = "myapp1"
    
    res = voxapi.add_application(APPLICATION_NAME)
    print(res)
