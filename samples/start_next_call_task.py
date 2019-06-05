from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Start next call task

    LIST_ID = 1
    
    try:
        res = voxapi.start_next_call_task(LIST_ID)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
