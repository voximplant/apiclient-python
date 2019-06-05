from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Add a new ACD queue for the application 1.

    ACD_QUEUE_NAME = "myqueue"
    APPLICATION_ID = 1
    
    try:
        res = voxapi.add_queue(ACD_QUEUE_NAME, application_id=APPLICATION_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
