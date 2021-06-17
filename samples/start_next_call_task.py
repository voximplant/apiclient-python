from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Start the next call task.

    LIST_ID = 1
    
    try:
        res = voxapi.start_next_call_task(LIST_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
