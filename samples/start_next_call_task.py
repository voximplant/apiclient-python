from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Start next call task

    LIST_ID = 1
    
    res = voxapi.start_next_call_task(LIST_ID)
    print(res)
