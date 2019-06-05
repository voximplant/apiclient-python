from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new application.

    APPLICATION_NAME = "myapp1"
    
    try:
        res = voxapi.add_application(APPLICATION_NAME)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
